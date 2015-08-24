# Virtual stock market bot

Simulates a stock market

Users can buy or sell shares by commenting either `BUY SOMETHING AMOUNT` or `SELL SOMETHING AMOUNT`, `SOMETHING` being the three letter code for the stock.
Users can also get their current shares by PMing the bot `LIST`.
Users start out with 1000 credits for buying shares.
Stock codes and their values are specified on the wiki page `prices`. Example sticky at the bottom.

Users' shares and their credit balance are stored in the wiki pages `shares` and `credit` in JSON.

## Installation and Usage

Scripts are designed to be run via cron, not run continuously. `pm.py` should probably be run fairly often (i.e. every two to three minutes), while `share.py` doesn't
need to be run that often.

Run `clear.py` once to create posts file.


### Example prices JSON
```
{  
  "AFG": {  
    "Value":553  
  },  
  "AME": {  
    "Value":350  
  },  
  "ARA": {  
    "Value":75  
  },  
  "ARG": {  
    "Value":472  
  },  
  "ARM": {  
    "Value":252  
  },  
  "ASH": {  
    "Value":387  
  },  
  "AUS": {  
    "Value":745  
  },  
  "AYY": {  
    "Value":446  
  },  
  "BLA": {  
    "Value":410  
  },  
  "BOE": {  
    "Value":533  
  },  
  "BRA": {  
    "Value":525  
  },  
  "BUC": {  
    "Value":741  
  },  
  "BUR": {  
    "Value":150  
  },  
  "BYZ": {  
    "Value":83  
  },  
  "CAN": {  
    "Value":868  
  },  
  "CAR": {  
    "Value":68  
  },  
  "CHA": {  
    "Value":54  
  },  
  "CHL": {  
    "Value":538  
  },  
  "CHN": {  
    "Value":551  
  },  
  "ENG": {  
    "Value":206  
  },  
  "ETH": {  
    "Value":617  
  },  
  "FIN": {  
    "Value":219  
  },  
  "FRA": {  
    "Value":424  
  },  
  "GER": {  
    "Value":383  
  },  
  "HAW": {  
    "Value":92  
  },  
  "HUN": {  
    "Value":547  
  },  
  "ICE": {  
    "Value":369  
  },  
  "INC": {  
    "Value":283  
  },  
  "IND": {  
    "Value":32  
  },  
  "INU": {  
    "Value":680  
  },  
  "IRE": {  
    "Value":381  
  },  
  "ISR": {  
    "Value":179  
  },  
  "JAP": {  
    "Value":251  
  },  
  "KIM": {  
    "Value":609  
  },  
  "KON": {  
    "Value":198  
  },  
  "KOR": {  
    "Value":40  
  },  
  "MAL": {  
    "Value":137  
  },  
  "MAO": {  
    "Value":197  
  },  
  "MAY": {  
    "Value":376  
  },  
  "MEX": {  
    "Value":474  
  },  
  "MON": {  
    "Value":337  
  },  
  "MOR": {  
    "Value":251  
  },  
  "MUG": {  
    "Value":567  
  },  
  "NOR": {  
    "Value":338  
  },  
  "PER": {  
    "Value":190  
  },  
  "PHI": {  
    "Value":227  
  },  
  "POL": {  
    "Value":401  
  },  
  "POR": {  
    "Value":365  
  },  
  "ROM": {  
    "Value":83  
  },  
  "SIB": {  
    "Value":438  
  },  
  "SIO": {  
    "Value":583  
  },  
  "SPA": {  
    "Value":487  
  },  
  "SRI": {  
    "Value":403  
  },  
  "SWE": {  
    "Value":116  
  },  
  "TEX": {  
    "Value":190  
  },  
  "TIB": {  
    "Value":84  
  },  
  "TIM": {  
    "Value":465  
  },  
  "USS": {  
    "Value":362  
  },  
  "VIE": {  
    "Value":323  
  },  
  "YAK": {  
    "Value":639  
  },  
  "ZUL": {  
    "Value":159  
  }  
}  
```
