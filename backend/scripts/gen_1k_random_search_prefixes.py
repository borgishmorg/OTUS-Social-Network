import random

from mimesis import Person
from mimesis.locales import Locale

COUNT = 1000
PERSON = Person(Locale.RU)

def main():
    for _ in range(COUNT):
        first_name = PERSON.first_name().lower()
        last_name = PERSON.last_name().lower()
        print(
            first_name[:random.randint(0, len(first_name)-1)],
            last_name[:random.randint(0, len(last_name)-1)],
            sep=',',
        )


if __name__ == '__main__':
    main()
