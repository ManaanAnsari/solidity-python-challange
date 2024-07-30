# DeFi-Solidity Challenge Solution

## Overview

This repository contains the solution to the DeFi-Solidity challenge. The goal was to create a set of smart contracts and a backend service to interact with them. The smart contracts include two ERC20 tokens and a vault for staking. The backend monitors events from the blockchain and distributes rewards accordingly.
challange: [link](https://github.com/ScottRMalley/defi-solidity-challenge)

## Design Decisions

### Solidity Development

- **Framework**: Foundry
  - **Reason**: Foundry is currently the most popular framework for Solidity development. It offers fast compilation and testing, making it easier to write and test Solidity code.
  - **Testing**: To run tests, simply install Foundry and execute `forge test`. This will compile and run the tests on the Solidity code.
- **Libraries**: OpenZeppelin
  - **Reason**: OpenZeppelin provides secure and tested implementations of standard contracts, which ensures reliability and security.

### Backend Development

- **Language**: Python
  - **Reason**: Python was chosen for the backend due to its robust data handling capabilities. Libraries such as Pandas are particularly useful for managing data without the need for a full-fledged database.
- **Framework**: None (Standalone Script)
  - **Reason**: Keeping it simple and modular. The backend script listens to blockchain events and distributes rewards without involving a complex database or messaging system.

## File Structure

- **Solidity Contracts**:

  - Located in the `src` directory.
  - `FudToken.sol`: Implementation of the FUD token.
  - `WinToken.sol`: Implementation of the WIN token with minting capabilities.
  - `AirVault.sol`: Implementation of the vault for staking FUD tokens.

- **Foundry Scripts**:

  - Located in the `scripts` directory.
  - `HelperConfig.s.sol`: Script to help deploy contracts and set active network configurations. This script aids in making the code modular and allows deployment/interactions on any network (local, Sepolia, etc.).

- **Backend**:
  - Located in the `backend` directory.
  - `server.py`: Main server file that listens to blockchain events and distributes rewards.
  - `web3_helper.py`: Helper functions for interacting with the blockchain.

note: I have written comments in all the files for more info

### Running the Backend

To run the backend:

1. Ensure Python and required libraries (`pandas`, `web3`) are installed.
   1. `pip install requirements.txt`
2. Set up your `.env` file with the necessary environment variables (e.g., private key) check `.env_template`.
3. Run the backend script: `python server.py`.

## Running foundry

### Solidity

- **Framework**: Foundry
- **How to Run**: `forge test`

## Private Key Management

- **Current Implementation**: The private key is stored in a `.env` file. This is not ideal for production environments.
- **Suggested Improvements**:
  - Encrypt and decrypt the private key whenever it is used. This approach offers a layer of security but is not foolproof.
  - Manage calculations within the Solidity contract itself and allow users to claim rewards from a portal. This method can save gas fees and avoid direct private key management in the backend.

## Gas Fee Optimization

- Initially, the focus was on getting a working solution.
- Manage calculations within the Solidity contract itself and allow users to claim rewards from a portal. This method can save gas fees and avoid direct private key management in the backend.

## Recommendations

- For a more comprehensive staking reward implementation, consider checking out [Synthetix Staking Reward](https://solidity-by-example.org/defi/staking-rewards/). This approach is more robust and efficient for distributing rewards.
- I have previously worked on this
