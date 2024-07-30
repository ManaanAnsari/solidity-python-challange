// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.18;

import {Script} from "forge-std/Script.sol";
import {AirVault} from "../src/AirVault.sol";
import {WinToken} from "../src/WinToken.sol";
import {FudToken} from "../src/FudToken.sol";

/*
this is script that helps deploy the contracts 
set the active network config

this helps the code to be modular 
 by just changing here 
i can deploy/ interact with the contract on any network (local/sepolia etc...)

this confilg also helps in testing the contract on different networks 

*/

contract HelperConfig is Script {
    struct NetworkConfig {
        address fudToken;
        address winToken;
    }

    NetworkConfig public activeNetworkConfig;

    constructor() {
        // set the active network config depending on chainid
        if (block.chainid == 11155111) {
            activeNetworkConfig = getSepoliaEthConfig();
        } else {
            activeNetworkConfig = getOrCreateAnvilNetworkConfig();
        }
    }

    function getSepoliaEthConfig() public pure returns (NetworkConfig memory) {
        // todos: to deploy on sepolia
        return NetworkConfig({fudToken: address(0), winToken: address(0)});
    }

    function getOrCreateAnvilNetworkConfig() public returns (NetworkConfig memory) {
        // will return if already deployed and have the activeNetworkConfig
        if (activeNetworkConfig.fudToken != address(0)) {
            return activeNetworkConfig;
        }
        // if not deployed then deploy the contract
        vm.startBroadcast();

        FudToken fudToken = new FudToken();
        WinToken winToken = new WinToken();

        vm.stopBroadcast();

        return NetworkConfig({fudToken: address(fudToken), winToken: address(winToken)});
    }
}
