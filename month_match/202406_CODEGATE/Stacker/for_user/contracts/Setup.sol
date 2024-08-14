// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import {Token} from "./Token.sol";
import {LpToken} from "./LpToken.sol";
import {StakingManager} from "./StakingManager.sol";

contract Setup {
    StakingManager public stakingManager;
    Token public token;

    constructor() payable {
        token = new Token();
        stakingManager = new StakingManager(address(token));

        token.transfer(address(stakingManager), 86400 * 1e18);

        token.approve(address(stakingManager), 100000 * 1e18);
        stakingManager.stake(100000 * 1e18);
    }

    function withdraw() external {
        token.transfer(msg.sender, token.balanceOf(address(this)));
    }

    function isSolved() public view returns (bool) {
        return token.balanceOf(address(this)) >= 10 * 1e18;
    }
}
