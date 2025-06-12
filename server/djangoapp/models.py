# Uncomment the following imports before adding the Model code
"""
car make and model Django models
"""
import re
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


# Create your models here.
# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class CarMake(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    country_name = models.CharField(max_length=50, blank=True)
    country_iso2 = models.CharField(max_length=2, blank=True)
    country_iso3 = models.CharField(max_length=3, blank=True)

    # Replace one or more spaces with a single space
    def remove_space_streaks(self, s):
        return re.sub(r'\s+', ' ', s)

    def clean(self):
        super().clean()  # Call the parent class's clean method

        self.name = \
            self.remove_space_streaks(self.name.strip().title()) \
            if self.name else ''
        self.description = \
            self.remove_space_streaks(self.description.strip()) \
            if self.description else ''
        self.country_name = \
            self.remove_space_streaks(self.country_name.strip().title()) \
            if self.country_name else ''
        self.country_iso2 = self.country_iso2.strip().upper() \
            if self.country_iso2 else ''
        self.country_iso3 = self.country_iso3.strip().upper() \
            if self.country_iso3 else ''

        if not self.name.strip():
            raise ValidationError({
                'name': 'Name cannot be empty or contain only whitespace.'
            })

    def save(self, *args, **kwargs):
        # Call full_clean to ensure data is fully cleaned and validated
        try:
            self.full_clean()
        except ValidationError as e:
            # Handle the validation error
            raise ValidationError(f"Validation failed: {e}") from e

        # Call the parent class's save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('WAGON', 'Wagon'),
        ('SUV', 'SUV'),
        ('COUPE', 'Coupe'),
        ('PICKUP', 'Pickup'),
        ('VAN', 'Van')
    ]
    CAR_FUEL_TYPES = [
        ('GASOLINE', 'Gasoline'),
        ('DIESEL', 'Diesel'),
        ('CNG', 'CNG'),
        ('BIO-DIESEL', 'Bio-Diesel'),
        ('LPG', 'LPG'),
        ('ETHANOL', 'Ethanol'),
        ('METHANOL', 'Methanol'),
        ('HYDROGEN', 'Hydrogen'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid (Plug-in & Non-Plug-in)'),
        ('SOLAR', 'Solar Powered')
    ]

    # Replace one or more spaces with a single space
    def remove_space_streaks(self, s):
        return re.sub(r'\s+', ' ', s)

    name = models.CharField(max_length=50)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_type = models.CharField(max_length=20, choices=CAR_TYPES)
    car_fuel_type = models.CharField(
        max_length=20,
        choices=CAR_FUEL_TYPES, blank=True
    )
    year = models.IntegerField(validators=[
        MaxValueValidator(2025),
        MinValueValidator(2000)
    ])

    def save(self, *args, **kwargs):

        # Call full_clean to ensure data is fully cleaned and validated
        try:
            self.full_clean()
        except ValidationError as e:
            # Handle the validation error
            raise ValidationError(f"Validation failed: {e}") from e

        # Call the parent class's save method
        super().save(*args, **kwargs)

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
