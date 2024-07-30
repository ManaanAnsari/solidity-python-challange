// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// FudToken is ERC20 token contract
contract FudToken is ERC20 {
    constructor() ERC20("FUD Token", "FUD") {
        _mint(msg.sender, 1500000 * 10 ** decimals());
    }
}
