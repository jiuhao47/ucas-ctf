// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import {LpToken} from "./LpToken.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract StakingManager {
    uint256 constant REWARD_PER_SECOND = 1e18;

    IERC20 public immutable TOKEN;
    LpToken public immutable LPTOKEN;

    uint256 lastUpdateTimestamp;
    uint256 rewardPerToken;

    struct UserInfo {
        uint256 staked;
        uint256 debt;
    }

    mapping(address => UserInfo) public userInfo;

    constructor(address token) {
        TOKEN = IERC20(token);
        LPTOKEN = new LpToken();
    }

    function update() internal {
        if (lastUpdateTimestamp == 0) {
            lastUpdateTimestamp = block.timestamp;
            return;
        }

        uint256 totalStaked = LPTOKEN.totalSupply();
        if (totalStaked > 0 && lastUpdateTimestamp != block.timestamp) {
            rewardPerToken = (block.timestamp - lastUpdateTimestamp) * REWARD_PER_SECOND * 1e18 / totalStaked;
            lastUpdateTimestamp = block.timestamp;
        }
    }

    function stake(uint256 amount) external {
        update();

        UserInfo storage user = userInfo[msg.sender];

        user.staked += amount;
        user.debt += (amount * rewardPerToken) / 1e18;

        LPTOKEN.mint(msg.sender, amount);
        TOKEN.transferFrom(msg.sender, address(this), amount);
    }

    function unstakeAll() external {
        update();

        UserInfo storage user = userInfo[msg.sender];

        uint256 staked = user.staked;
        uint256 reward = (staked * rewardPerToken / 1e18) - user.debt;
        user.staked = 0;
        user.debt = 0;

        LPTOKEN.burnFrom(msg.sender, LPTOKEN.balanceOf(msg.sender));
        TOKEN.transfer(msg.sender, staked + reward);
    }
}
