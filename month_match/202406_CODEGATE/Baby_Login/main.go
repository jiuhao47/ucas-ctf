package main

import (
	"bufio"
	"crypto/aes"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"crypto/subtle"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/big"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"github.com/google/uuid"
)

type HTTPRequest struct {
	Method   string `json:"method"`
	Uid      string `json:"uid"`
	Password string `json:"password"`
	Session  string `json:"session"`
	Secret   string `json:"secret"`
	Path     string `json:"path"`
}

type User struct {
	userName string
	userRole string
}

var SessionManager map[string]User
var SERVER_SECRET_KEY []byte

func pad(s []byte, length int) []byte {
	for len(s)%length != 0 || len(s) < length {
		s = append(s, byte('\x00'))
	}
	return s
}

func unpad(s []byte) []byte {
	for s[len(s)-1] == byte('\x00') {
		s = s[:len(s)-1]
	}
	return s
}

func KDF(Gx, Gy *big.Int, serverPriv []byte) ([]byte, []byte) {
	_m, _ := elliptic.P256().ScalarMult(Gx, Gy, serverPriv)
	key := pad(_m.Bytes(), 32)
	return key[:16], key[16:32]
}

func passwordGen(uid, role string) []byte {
	curve := elliptic.P256()
	R, _ := ecdsa.GenerateKey(curve, rand.Reader)
	Gx, Gy := R.PublicKey.X, R.PublicKey.Y

	key1, key2 := KDF(Gx, Gy, SERVER_SECRET_KEY)

	cipher, _ := aes.NewCipher(key1)
	ct := make([]byte, 16)

	cipher.Encrypt(ct, pad([]byte(uid+"_GUEST"), 16))

	out := append(Gx.Bytes(), Gy.Bytes()...)
	out = append(out, ct...)
	hmac := hmac.New(sha256.New, key2)
	hmac.Write(out)
	tag := hmac.Sum(nil)

	out = append(out, tag...)
	return out
}

func indexHandler(r HTTPRequest) {
	if r.Method == "GET" {
		u := SessionManager[r.Session]
		if u.userName == "" {
			fmt.Println("Register first and login to access the website!")
			return
		} else {
			fmt.Println("Hi " + u.userName + "! You are logged in as " + u.userRole)
		}
		return
	} else {
		fmt.Println("Method Not Allowed")
		return
	}
}

func registerHandler(r HTTPRequest) {
	if r.Method == "GET" {
		fmt.Println("You can register with your username!")
		return
	} else if r.Method == "POST" {
		uid := r.Uid
		if uid == "" {
			fmt.Println("Bad Request")
			return
		} else if uid == "ADMIN" {
			fmt.Println("Nope! You can't register as ADMIN!")
			return
		}
		password := passwordGen(uid, "GUEST")
		fmt.Println("Here is your password token : " + base64.StdEncoding.EncodeToString(password))
		return
	} else {
		fmt.Println("Method Not Allowed")
		return
	}
}

func loginHandler(r HTTPRequest) {
	if r.Method == "GET" {
		fmt.Println("You can login with your username and password token!")
		return
	} else if r.Method == "POST" {
		uname := SessionManager[r.Session].userName
		if uname != "" {
			fmt.Println("You are already logged in as " + uname)
			return
		}
		uid := r.Uid
		password := r.Password
		if uid == "" || password == "" {
			fmt.Println("Bad Request")
			return
		}

		pw, err := base64.StdEncoding.DecodeString(password)
		if err != nil {
			fmt.Println("Bad Request")
			return
		}

		length := len(pw)
		if length < 112 || length%16 != 0 {
			fmt.Println("Bad Request")
			return
		}

		Gx := new(big.Int).SetBytes(pw[:32])
		Gy := new(big.Int).SetBytes(pw[32:64])
		ct, hmac_in := pw[64:length-32], pw[length-32:]

		key1, key2 := KDF(Gx, Gy, SERVER_SECRET_KEY)
		hmac := hmac.New(sha256.New, key2)
		hmac.Write(pw[:length-32])
		tag := hmac.Sum(nil)

		if subtle.ConstantTimeCompare(tag, hmac_in) != 1 {
			fmt.Println("Unauthorized")
			return
		}

		cipher, _ := aes.NewCipher(key1)
		pt := make([]byte, len(ct))
		cipher.Decrypt(pt, ct)
		tmp := strings.Split(string(unpad(pt)), "_")
		if len(tmp) < 2 {
			fmt.Println("Unauthorized")
			return
		}
		userId, userRole := tmp[0], tmp[1]

		if userId != uid {
			fmt.Println("Unauthorized")
			return
		}
		u, _ := uuid.NewRandom()
		var user User
		user.userName = userId
		user.userRole = userRole
		SessionManager[u.String()] = user
		fmt.Println("Hello " + userId + "! You are logged in as " + userRole + "!!")
		fmt.Println("Here is your session : " + u.String())
		return
	} else {
		fmt.Println("Method Not Allowed")
		return
	}
}

func logoutHandler(r HTTPRequest) {
	if r.Method == "GET" {
		uname := SessionManager[r.Session].userName
		if uname == "" {
			fmt.Println("You are not logged in!")
			return
		}
		delete(SessionManager, r.Session)
		fmt.Println("Logged out successfully!")
		return
	} else {
		fmt.Println("Method Not Allowed")
		return
	}
}

func flagHandler(r HTTPRequest) {
	if r.Method == "POST" {
		uname := SessionManager[r.Session].userName
		userRole := SessionManager[r.Session].userRole
		if uname != "ADMIN" || userRole != "admin" {
			fmt.Println("Unauthorized")
			return
		}
		secret := r.Secret
		sec, err := base64.StdEncoding.DecodeString(secret)
		if err != nil {
			fmt.Println("Bad Request")
			return
		}

		if subtle.ConstantTimeCompare(SERVER_SECRET_KEY, sec) != 1 {
			fmt.Println("Unauthorized")
			return
		}
		FLAG, _ := ioutil.ReadFile("./flag")
		fmt.Println("Here is your flag : " + string(FLAG))
	} else {
		fmt.Println("Method Not Allowed")
		return
	}
}

func getRequest(r *bufio.Reader) (HTTPRequest, error) {
	var err error
	var input string
	var request HTTPRequest

	fmt.Print("> ")

	input, err = r.ReadString('\n')
	if err != nil {
		fmt.Println("Invalid input1")
		return HTTPRequest{}, err
	}
	err = json.Unmarshal([]byte(input), &request)
	if err != nil {
		fmt.Println("Invalid input2")
		return HTTPRequest{}, err
	}
	return request, nil
}

func generateRandomString(length int) string {
	const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	b := make([]byte, length)
	for i := range b {
		num, err := rand.Int(rand.Reader, big.NewInt(int64(len(charset))))
		if err != nil {
			panic(err)
		}
		b[i] = charset[num.Int64()]
	}
	return string(b)
}

func validateHash(hashValue *big.Int) bool {
	shifted := new(big.Int).Rsh(hashValue, 24)
	shifted.Lsh(shifted, 24)
	return shifted.Cmp(hashValue) == 0
}

// PoW performs a proof-of-work verification.
// It generates a random string, prompts the user for an answer,
// concatenates the random string and the answer, computes the SHA256 hash,
// and validates the hash against a predefined condition.
// If the hash is invalid, it prints an error message and exits the program.
func PoW() {
	randomString := generateRandomString(16)
	fmt.Println("PoW > " + randomString)

	var answer string
	fmt.Scanln(&answer)

	concatenated := randomString + answer
	hash := sha256.Sum256([]byte(concatenated))
	hashValue := new(big.Int).SetBytes(hash[:])

	if !validateHash(hashValue) {
		fmt.Println("Invalid PoW")
		os.Exit(1)
	}

}

func main() {
	//PoW()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGALRM)

	go func() {
		time.Sleep(600 * time.Second)
		fmt.Println("timeout")
		os.Exit(1)
	}()

	SessionManager = make(map[string]User)
	SERVER_SECRET_KEY = make([]byte, 33)

	_, _ = rand.Read(SERVER_SECRET_KEY)

	fmt.Println("webAPI for my \"Baby Login\" system")
	reader := bufio.NewReader(os.Stdin)

	for {
		request, err := getRequest(reader)
		if err != nil {
			fmt.Println("Invalid input3")
			return
		}
		switch request.Path {
		case "/", "/index.html":
			indexHandler(request)
		case "/register.html":
			registerHandler(request)
		case "/login.html":
			loginHandler(request)
		case "/logout.html":
			logoutHandler(request)
		case "/flag.html":
			flagHandler(request)
		default:
			fmt.Println("Invalid path")
		}
	}
}
//{method: "GET",uid: "GUEST",password: "",session: "",secret: "",path: "/"}
//{method:"GET",uid:"GUEST",password:"",session:"",secret:"",path:"/"}
//{"method":"POST","uid":"GUEST","password":"","session":"","secret":"","path":"/register.html"}
//{"method":"POST","uid":"GUEST","password":"m4mTk8nc7Xb2HGgq2ZezhlkM3Q3Ox+FjAgofw5pbIB1Hb5PJdDX9qKDMlvQP+6GuqK5gQrkI2kjD2k8UhMvNN8lWeVQfA0NtvEflTxncTH+J6Pdq/AjYmLOtLcMt8r0GVWgltnIUejoNg5oQQ8AFng==","session":"","secret":"","path":"/login.html"}
//m4mTk8nc7Xb2HGgq2ZezhlkM3Q3Ox+FjAgofw5pbIB1Hb5PJdDX9qKDMlvQP+6GuqK5gQrkI2kjD2k8UhMvNN8lWeVQfA0NtvEflTxncTH+J6Pdq/AjYmLOtLcMt8r0GVWgltnIUejoNg5oQQ8AFng==
//d7ed810a-9502-48fd-83e5-d2d14cf594bb
//{"method":"POST","uid":"ADMIN","password":"m4mTk8nc7Xb2HGgq2ZezhlkM3Q3Ox+FjAgofw5pbIB1Hb5PJdDX9qKDMlvQP+6GuqK5gQrkI2kjD2k8UhMvNN8lWeVQfA0NtvEflTxncTH+J6Pdq/AjYmLOtLcMt8r0GVWgltnIUejoNg5oQQ8AFng==","session":"","secret":"","path":"/login.html"}
