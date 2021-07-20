# famcs-applicants-bot
Bot for applicants. It helps to see how many people have a higher score.
## Basic usage
There are two ways you can use this repo.
Bot can be freely accesed at [http://t.me/FamcsChecker_bot](http://t.me/FamcsChecker_bot) while the campaign.

Or you can use the following snippet to use standalone parser module:
```python
from monitoringparser import Parser

spec_name = "информатика"
grade     = 378 

def grade_to_range(grade: int) -> str:
    if grade >= 391:               
        return "391+"
    if grade <= 120:
        return "120-" 
    remainder = grade % 5
    if remainder == 0:
        return f'{grade}-{grade - 4}'
    return f'{grade - remainder + 5}-{grade - remainder + 1}'

parser = Parser()
print(parser(spec_name, grade_to_range(grade)))
```
Example output
```
План приема на факультет: 266
Подано заявлений: 44
Специальность: информатика
План приема на бюджет: 95
Целевики: 0
План приема на платное: 25
Всего подано заявлений: 20
Олимпиадники: 3
391+: 1
390-386: 1
380-376: 3
375-371: 1
370-366: 3
360-356: 2
355-351: 4
345-341: 2
Вы указали балл: 380-376
Вас опережает 5 + 3 человек
```
## Contributing
You can help to maintain this bot by providing a hosting service or by modifying parser due to updates of table format from the [BSU page](https://abit.bsu.by/formk1?id=1").

## Credits
Original credits go to:
- [ijimiji a.k.a. Jahor Laryn](https://github.com/ijimiji) for creating the parser.
- [Ilya Gordey](https://github.com/al1enjesus) for creating the telegram bot.
