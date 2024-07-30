// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.18;

import {Test, console} from "forge-std/Test.sol";
import {DeployAirVault} from "../../script/DeployAirVault.s.sol";
import {HelperConfig} from "../../script/HelperConfig.s.sol";
import {AirVault} from "../../src/AirVault.sol";
import {FudToken} from "../../src/FudToken.sol";

/*
A basic tect contract to test withdrawal and deposit of AirVault
*/

contract AirVaultTest is Test {
    AirVault airVault;
    HelperConfig helperConfig;
    address fudToken;
    uint256 depositAmount = 1000 ether;

    function setUp() public {
        // this functioon runs everytime before each test
        DeployAirVault deployAirVault = new DeployAirVault();
        (airVault, helperConfig, fudToken,) = deployAirVault.run();
        // mint some test fudtoken for testing on this contract
        deal(address(fudToken), address(this), depositAmount);
    }

    function testAirVaultDeposit() public {
        // approve the airvault to spend the fudtoken
        FudToken(fudToken).approve(address(airVault), depositAmount);
        // deposit the fudtoken to the airvault
        airVault.deposit(depositAmount);
        // check if the balance of the airvault is equal to the deposit amount
        assertEq(airVault.lockedBalanceOf(address(this)), depositAmount);
    }

    function testAirVaultWithdraw() public {
        // approve the airvault to spend the fudtoken
        FudToken(fudToken).approve(address(airVault), depositAmount);
        // deposit the fudtoken to the airvault
        airVault.deposit(depositAmount);
        // withdraw the fudtoken from the airvault
        airVault.withdraw(depositAmount);
        // check if the balance of the airvault is equal to the deposit amount
        assertEq(airVault.lockedBalanceOf(address(this)), 0);
    }
}
