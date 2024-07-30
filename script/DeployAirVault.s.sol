// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.18;

import {Script} from "forge-std/Script.sol";
import {HelperConfig} from "./HelperConfig.s.sol";
import {AirVault} from "../src/AirVault.sol";

/*
This is a foundry script that helps deploy the AirVault contract.
*/

contract DeployAirVault is Script {
    address[] public priceFeeds;
    address[] public tokens;

    function run() external returns (AirVault, HelperConfig, address, address) {
        HelperConfig helperConfig = new HelperConfig();
        (address fudToken, address winToken) = helperConfig.activeNetworkConfig();

        vm.startBroadcast();
        AirVault airVault = new AirVault(fudToken);
        vm.stopBroadcast();
        return (airVault, helperConfig, fudToken, winToken);
    }
}
