from dataclasses import dataclass, field
import random
import string


def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))

@dataclass
class Person:
    name: str
    address: str
    active: bool = True
    email_addresses: list[str] = field(default_factory=list)
    id: str = field(init=False, default_factory=generate_id)

def main() -> None:
    joe = Person("Joe", "123 Street")
    print(joe)
    jerry = Person("Jerry", "456 Road")
    print(jerry)
    print(joe)

if __name__=="__main__":
    main()
