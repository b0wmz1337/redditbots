# Virtual stock market bot

Simulates a stock market

Users can buy or sell shares by commenting either `BUY SOMETHING AMOUNT` or `SELL SOMETHING AMOUNT`, `SOMETHING` being the three letter code for the stock.
Users can also get their current shares by PMing the bot `LIST`.
Users start out with 1000 credits for buying shares.
Stock codes and their individual values are specified in the same sticky. Example sticky at the bottom.

Users' shares and their credit balance are stored in the wiki pages `shares` and `credit` in JSON.

## Installation and Usage

Scripts are designed to be run via cron, not run continuously. `pm.py` should probably be run fairly often (i.e. every two to three minutes), while `share.py` doesn't
need to be run that often.

Run `clear.py` once to create posts file.


### Example sticky
```
**CODE**|**Civilization**|**Value**|
:--|:--|--:|
AFG|Afghanistan|489|
AME|America|305|
ARA|Arabia|80|
ARG|Argentina|476|
ARM|Armenia|238|
ASH|Ashanti|166|
AUS|Australia|717|
AYY|Ayyubids|512|
BLA|Blackfoot|448|
BOE|Boers|400|
BRA|Brazil|520|
BUC|Buccaneers|816|
BUR|Burma|266|
BYZ|Byzantium|66|
CAN|Canada|884|
CAR|Carthage|80|
CHA|Champa|25|
CHL|Chile|463|
CHN|China|606|
ENG|England|176|
ETH|Ethiopia|608|
FIN|Finland|221|
FRA|France|506|
GER|Germany|359|
HAW|Hawaii|110|
HUN|Huns|530|
ICE|Iceland|446|
INC|Inca|235|
IND|Indonesia|36|
INU|Inuit|697|
IRE|Ireland|519|
ISR|Israel|205|
JAP|Japan|359|
KIM|Kimberly|622|
KON|Kongo|308|
KOR|Korea|31|
MAL|Mali|123|
MAO|Maori|305|
MAY|Mayans|381|
MEX|Mexico|391|
MON|Mongolia|375|
MOR|Morocco|208|
MUG|Mughals|555|
NOR|Norway|176|
PER|Persia|298|
PHI|Philippines|265|
POL|Poland|345|
POR|Portugal|268|
ROM|Rome|135|
SIB|Sibir|404|
SIO|Sioux|587|
SPA|Sparta|566|
SRI|Sri Lanka|537|
SWE|Sweden|132|
TEX|Texas|348|
TIB|Tibet|162|
TIM|Timurids|327|
USS|U.S.S.R|229|
VIE|Vietnam|413|
YAK|Yakutia|639|
ZUL|Zulus|202|
```
