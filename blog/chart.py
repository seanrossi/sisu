import pygal

from .models import Category, Post

class CatPieChart():
  def __init__(self, **kwargs):
      self.chart = pygal.Pie(**kwargs)
      self.chart.print_values = True
      #self.chart.title = 'You Activity'
        
  def get_data(self, user_data):
      data = {}
      categories = Category.__members__.items()
           
      for name, member in categories:
        data[member.value] = 0
        #print("in chart.py: " + member.label + " " + name)
           
      for post in user_data:
        print(post.category_name)
        if(post.category_name.name in data):
          data[post.category_name.name] += 1
        else:
          data[post.category_name.name] = 1
      
      return data
  
  def generate(self, user_data):
      chart_data = self.get_data(user_data)
      
      for key, value in chart_data.items():
        #self.chart.add(key, value)
        self.chart.add(key, value, formatter=lambda x: '%s' % x)
        
      return self.chart.render(is_unicode=True)  