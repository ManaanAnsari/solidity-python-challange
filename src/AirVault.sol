// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/*
the main AirVault contract
*/

contract AirVault is Ownable {
    using SafeERC20 for IERC20;

    // the token being deposited
    IERC20 public fudToken;
    // user balances
    mapping(address => uint256) private balances;
    // total deposited
    uint256 public totalDeposited;

    // events
    event Deposit(address indexed user, uint256 amount, uint256 locked_balance);
    event Withdraw(address indexed user, uint256 amount, uint256 locked_balance);

    constructor(address _fudToken) Ownable(msg.sender) {
        fudToken = IERC20(_fudToken);
    }

    function deposit(uint256 amount) public returns (bool) {
        // CEI (checks effects interactions)
        fudToken.safeTransferFrom(msg.sender, address(this), amount);
        balances[msg.sender] += amount;
        totalDeposited += amount;
        // log the user, amount and the locked balance
        emit Deposit(msg.sender, amount, balances[msg.sender]);
        return true;
    }

    function withdraw(uint256 amount) public returns (bool) {
        // CEI (checks effects interactions)
        require(balances[msg.sender] >= amount, "Insufficient balance");
        fudToken.safeTransfer(msg.sender, amount);
        balances[msg.sender] -= amount;
        totalDeposited -= amount;
        emit Withdraw(msg.sender, amount, balances[msg.sender]);
        return true;
    }

    function lockedBalanceOf(address account) external view returns (uint256) {
        return balances[account];
    }
}
