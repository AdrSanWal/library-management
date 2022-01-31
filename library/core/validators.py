from datetime import date
from re import match

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


# Author validators --------------------------------------------------------------------------#

def clean_author_dates(self):
    """If died and born fields are filled, check that the date
    of death is not before the date of birth
    """
    if self.died and self.born:
        if self.died < self.born:
            raise ValidationError(
                {"died": "Death date cannot be earlier than birth date"})


@deconstructible
class DatesValidator():
    """check that the date is less than or equal to the current date"""
    def __init__(self, field=None):
        self.field = field

    def __call__(self, value):
        if value > date.today():
            raise ValidationError('The date has not yet arrived')
        else:
            return value

# Book validators ----------------------------------------------------------------------------#


def control_digit(numbers, n=0, tot=0):
    """Check if isbn control digit is correct. Return True if it's valid in [0]
    and correct control digit in [1]
    """
    mult = {0: 1, 1: 3}
    while n < len(numbers):
        tot += int(numbers[n]) * mult[n % 2]
        return control_digit(numbers, n + 1, tot)
    digit = 10 - (tot - int(numbers[n - 1])) % 10
    return not bool(tot % 10), 0 if digit == 10 else digit


def clean_series_order(self):
    """If the field serie is filled, it checks that series_order is also
    filled and that it does not already exist for that serie
    """
    if self.serie:
        if not self.serie_order:
            raise ValidationError(
                {"serie_order": "If the book is from a serie, it must have serie_order"})
        else:
            # Exclude the instance itself so it doesn't throw an error when updating a book
            from .models import Book  # To avoid circular import
            books = Book.objects.filter(serie=self.serie).exclude(isbn=self.isbn)
            orders = [book.serie_order for book in books]
            if self.serie_order in orders:
                raise ValidationError(
                    {"serie_order": f"This order in the serie is already taken.\nUsed orders: {orders}"})  


@deconstructible
class IsbnValidator():
    """Check that the isbn field follow the required pattern,
    and that the control digit is correct
    """
    def __init__(self, data=None):
        self.pattern = r'^(?=.{17}$)(^97(9|8)-\d{1,5}-\d{1,7}-\d{1,6}-\d$)'
        self.data = data

    def __call__(self, value):
        pattern_match = match(self.pattern, value)
        if bool(pattern_match):
            numbers = value.replace('-', '')
            ctrl_digit = control_digit(numbers)
            if ctrl_digit[0]:
                return value
            raise ValidationError(f"Format correct but control digit should be {ctrl_digit[1]}")
        else:
            raise ValidationError("Your string should match the conditions")
