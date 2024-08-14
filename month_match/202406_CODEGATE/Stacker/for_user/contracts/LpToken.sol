// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract LpToken is ERC20 {
    address immutable minter;

    constructor() ERC20("LP Token", "LP") {
        minter = msg.sender;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == minter, "only minter");
        _mint(to, amount);
    }

    function burnFrom(address from, uint256 amount) external {
        _burn(from, amount);
    }
}
