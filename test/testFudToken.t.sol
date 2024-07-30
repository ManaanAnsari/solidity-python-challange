// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.18;

import {Test, console} from "forge-std/Test.sol";
import {HelperConfig} from "../script/HelperConfig.s.sol";
import {FudToken} from "../src/FudToken.sol";

/*
A basic tect contract to test FudToken
*/

contract fudTest is Test {
    HelperConfig helperConfig;
    FudToken fudToken;

    function setUp() public {
        helperConfig = new HelperConfig();
        (address _f,) = helperConfig.activeNetworkConfig();
        fudToken = FudToken(_f);
    }

    function testFudToken() public view {
        assertEq(fudToken.totalSupply(), 1500000 ether);
    }
}
