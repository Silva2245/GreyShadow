class FoodType:
    def __init__(self, name : str, typee : str, region : str):
        self.foodtype = None
        self.typee = None
        self.region = None
        

class SaltyFood(FoodType):
    def __init__(self, name : str, typee : str, region : str):
        super().__init__(name, typee, region)
        self.foodtype = 'Salty'
        
class SugaryFood(FoodType):
    def __init__(self, name : str, typee : str, region : str):
        super().__init__(name, typee, region)
        self.foodtype = 'Sugary'

class Food:
    def __init__(self, foodType : FoodType):
        self.foodtype = foodType.foodtype
        print(f'your food type is {self.foodtype}')
        
try:
    ft = SugaryFood('nn', 'nn', 'nn')
    f = Food(ft)

    ft = SaltyFood('tt', 'tt', 'tt')
    f = Food(ft)
except Exception as e:
    print(f'the error was {str(e)}')