# Credit Card Numbers

![credit cards](https://live.staticflickr.com/3372/3518120757_6f6d723b0e_n.jpg)

# What to Do

A credit (or debit) card, of course, is a plastic card with which you can pay for goods and services. Printed on that card is a number that’s also stored in a database somewhere, so that when your card is used to buy something, the creditor knows whom to bill. 

There are a lot of people with credit cards in this world, so those numbers are pretty long: 
- American Express uses **15-digit** numbers, 
- MasterCard uses **16-digit** numbers, 
- Visa uses **13- and 16-digit** numbers. 

And those are decimal numbers (0 through 9), not binary, which means, for instance, that American Express could print as many as 10^15 = 1,000,000,000,000,000 unique cards! (That’s, um, a quadrillion.)

Actually, that’s a bit of an exaggeration, because credit card numbers actually have some structure to them. 
- All American Express numbers start with `34` or `37`.
- Most MasterCard numbers start with `51`, `52`, `53`, `54`, or `55` (they also have some other potential starting numbers which we won’t concern ourselves with for this problem)
- All Visa numbers start with `4`.

But credit card numbers also have a "***checksum***” built into them, a mathematical relationship between at least one number and others. That checksum enables computers (or humans who like math) to detect typos (e.g., transpositions), if not fraudulent numbers, without having to query a database, which can be slow. Of course, a dishonest mathematician could certainly craft a fake number that nonetheless respects the mathematical constraint, so a database lookup is still necessary for more rigorous checks.

You have to implement a program that checks the validity of a given credit card number.

## Luhn's Algorithm

So what’s the secret formula? Well, most cards use an algorithm invented by [Hans Peter Luhn](https://en.wikipedia.org/wiki/Hans_Peter_Luhn) of IBM. According to Luhn’s algorithm, you can determine if a credit card number is (syntactically) valid as follows:
1. Take every other digit, from right-to-left, starting with the second-to-last digit.
2. Multiply each digit by 2.
3. Add those products’ digits together.
4. Get the sum of the digits that weren’t multiplied by 2.
5. Sum results from steps 3 and 4. If the total’s last digit is 0, the number is valid!

That’s kind of confusing, so let’s try an example with 4003600000000014 (VISA).
1. Take every other digit, starting with the second-to-last digit, from right-to-left.
```
4003600000000014
4 0 6 0 0 0 0 1
```
1. Multiply each digit by 2.
```
4 0 6  0 0 0 0 1
8 0 12 0 0 0 0 2
```
1. Add those products’ digits together.
```
8 0 12  0 0 0 0 2
8+0+1+2+0+0+0+0+2 = 13
```
1. Get the sum of the digits that weren’t multiplied by 2.
```
4003600000000014
 0+3+0+0+0+0+0+4 = 7
```
1. Sum results from steps 3 and 4. 
```
7 + 13 = 20
```
The total’s last digit is `0`, `4003600000000014` is valid and it's a `VISA` number
because it starts with `4`

## Implémentation

In the file called `credit.py`, write a program that prompts the user for a credit card number and then reports whether it is a valid American Express (`AMEX`), MasterCard (`MASTERCARD`), or Visa (`VISA`) card number, per the definitions of each’s format herein. So that we can automate some tests of your code, we ask that your program’s last line of output be `AMEX` or `MASTERCARD` or `VISA` or `INVALID`, nothing more, nothing less. 

For simplicity, you may assume that the user’s input will be entirely numeric (i.e., devoid of hyphens, as might be printed on an actual card) and that it won’t have leading zeroes.

Consider the below representative of how your own program should behave when passed a valid credit card number.

```bash
$ python credit.py
Number: 4003600000000014
VISA
```
Re-prompt the user, again and again as needed, if their input is not an `int`. 
```bash
$ python credit.py
Number: 4003-6000-0000-0014
Number: foo
Number: 4003600000000014
VISA
```

An example of invalid number:
```bash
$ python credit.py
Number: 6176292929
INVALID
````

# When to Do it

By Sunday, january 12, 2025 at 11:59 PM

# How to Test

- Test your script with command `./check credit.py`

Here are a few valid card numbers:
- `4301050403060 VISA`
- `4070605020003060 VISA`
- `5150400020204060 MASTERCARD`
- `5530603080700080 MASTERCARD`
- `340901000708030 AMEX`
- `340702050700020 AMEX`

> [!TIPS]
> You may find many card numbers for test on the web.
> Check and double-check your code on every card number you may find.

# How to Submit

Once you're done with all tasks, submit all your python files on Moodle

> [!NOTE]
> If you know how to check a number, you also know how to generate it. 
> So you can write a random code generator given a card type as input. 
> Obviously, you should implement it ONLY if you have time to do so... 
> it will only increase your XP and let you level up (maybe)
