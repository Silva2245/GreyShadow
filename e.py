class FoodType:
    def __init__(self):
        self.foodtype = None

class SaltyFood(FoodType):
    def __init__(self):
        super().__init__()
        self.foodtype = 'Salty'
        
class SugaryFood(FoodType):
    def __init__(self):
        super().__init__()
        self.foodtype = 'Sugary'

class Food:
    def __init__(self, foodType : FoodType):
        self.foodtype = foodType.foodtype
        print(f'your food type is {self.foodtype}')
        
ft = SugaryFood()
f = Food(ft)

ft = SaltyFood()
f = Food(ft)