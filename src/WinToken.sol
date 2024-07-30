// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract WinToken is ERC20, Ownable {
    constructor() ERC20("WIN Token", "WIN") Ownable(msg.sender) {
        // create a contract with the name "WIN Token" and symbol "WIN"
        // only the owner can mint new tokens
    }

    function mint(address account, uint256 amount) public onlyOwner returns (bool) {
        // only the owner can mint new tokens on any account address
        _mint(account, amount);
        return true;
    }
}
