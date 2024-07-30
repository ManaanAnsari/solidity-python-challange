```bash
forge compile

source .env

forge create WinToken --private-key $PRIV

forge create WinToken --interactive

forge create AirVault --constructor-args $FUD --private-key $PRIV

cast call $FUD "balanceOf(address)" $AIR

cast send $FUD "approve(address,uint256)" $AIR $AMT --private-key $PRIV

cast send $AIR "deposit(uint256)" $AMT --private-key $PRIV

cast send $AIR "withdraw(uint256)" $AMT --private-key $PRIV
```
