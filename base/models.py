from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=200, null=True)
    # name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Category(models.Model):

    name = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Location(models.Model):

    name = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class ExpensesViewManager(models.Manager):

    def grouped_by_category(self, start_dt, end_dt, username):
        if username:
            return self.raw(f"""
                SELECT 
                    t1.category_id as id,
                    t2.`name` AS category_name,
                    SUM(t1.cost) AS total_cost
                FROM
                    costs_of_living.base_expenses t1
                        LEFT JOIN
                    costs_of_living.base_category t2 ON t1.category_id = t2.id
                        LEFT JOIN
                    costs_of_living.base_user t3 ON t1.purchaser_id = t3.id
                WHERE
                    t3.username = '{username}'
                    AND
                    t1.date_purchased BETWEEN '{start_dt}' AND '{end_dt}'
                GROUP BY t2.`name`
                ORDER BY t2.`name` ASC
                """
            )
        else:
            return self.raw(f"""
                SELECT 
                    t1.category_id as id,
                    t2.`name` AS category_name,
                    SUM(t1.cost) AS total_cost
                FROM
                    costs_of_living.base_expenses t1
                        LEFT JOIN
                    costs_of_living.base_category t2 ON t1.category_id = t2.id
                WHERE
                    t1.date_purchased BETWEEN '{start_dt}' AND '{end_dt}'
                GROUP BY t2.`name`
                ORDER BY t2.`name` ASC
                """
            )
    
    def grouped_short_tag(self, start_dt, end_dt, username):
        if username:
            return self.raw(f"""
                SELECT
                    t1.id,
                    t1.short_tag,
                    sum(t1.cost) as cost,
                    count(t1.short_tag) as count
                FROM
                    costs_of_living.base_expenses t1
                LEFT JOIN
                    costs_of_living.base_user t2 ON t1.purchaser_id = t2.id
                WHERE
                    t2.username = '{username}'
                    AND
                    t1.date_purchased BETWEEN '{start_dt}' AND '{end_dt}'
                GROUP BY
                    t1.short_tag
                ORDER BY sum(t1.cost) DESC
                """
            )
        else:
            return self.raw(f"""
                SELECT
                    id,
                    short_tag,
                    sum(cost) as cost,
                    count(short_tag) as count
                FROM
                    costs_of_living.base_expenses
                WHERE
                    date_purchased BETWEEN '{start_dt}' AND '{end_dt}'
                GROUP BY
                    short_tag
                ORDER BY sum(cost) DESC
                """
            )
    
    def grouped_by_user(self, start_dt, end_dt):
        return self.raw(f"""
            SELECT 
                t1.purchaser_id as id,
                t2.username,
                SUM(cost) AS spend
            FROM
                costs_of_living.base_expenses t1
                    LEFT JOIN
                costs_of_living.base_user t2 ON t1.purchaser_id = t2.id
            WHERE
                t1.date_purchased BETWEEN '{start_dt}' AND '{end_dt}'
            GROUP BY t2.username
            ORDER BY SUM(cost) DESC;
            """
        )

    def all_by_user(self, start_dt, end_dt):
        return self.raw(f"""
            SELECT 
                t1.purchaser_id as id,
                t2.username,
                t1.thing,
                t1.cost
            FROM
                costs_of_living.base_expenses t1
                    LEFT JOIN
                costs_of_living.base_user t2 ON t1.purchaser_id = t2.id
            WHERE
                t1.date_purchased BETWEEN '{start_dt}' AND '{end_dt}'
            ORDER BY date_purchased DESC;
            """
        )


class Expenses(models.Model):
    purchaser = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    intended_recipient = models.CharField(max_length=60, blank=True, null=True)
    thing = models.CharField(max_length=100, blank=True, null=True)
    short_tag = models.CharField(max_length=20, blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    date_purchased = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    year_month = models.CharField(max_length=7, blank=True, null=True)

    objects = ExpensesViewManager()

    def __str__(self):
        return self.thing
        
    class Meta:
        ordering = ['-date_added']
