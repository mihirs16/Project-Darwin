import datetime
import random
import pandas as pd

def generateData(num_data,toCSV=False):
  ovr_score = []
  doj = []
  skill = []
  yoe = []
  for n in range(num_data):
      ovr_score.append(random.randrange(75, 100))
      doj.append(datetime.datetime.now() + datetime.timedelta(days=random.randrange(1, 30)))
      skill.append([
              random.choice(["AI", "Business Intelligence", "Machine Learning"]),
              random.choice(["Data Science", "Backend Developer", "Digital Marketing"]),
              random.choice(["Frontend Developer", "UI/UX", "Web Developer"])
      ])
      yoe.append(random.randrange(22, 40))
  d = pd.DataFrame(data={"overall_score":ovr_score,"Date_Of_Joining":doj,"Skill":skill,"Year_of_Experience":yoe})
  if toCSV:
    d.to_csv("MockData.csv",index=False)
  return d

#print(generateData(50).head())