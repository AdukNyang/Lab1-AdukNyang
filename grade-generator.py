import csv
FA_Grades=[]
FA_names=[]
SA_Grades=[]
FA_weight=[]
SA_weight=[]
SA_count= 0
FA_count= 0
SA_Names=[]
# Now final weight of the grades
Fa_real_weight=[]
Sa_real_weight=[]



class validation():
    def __init__(self,input_value):
        self.input = input_value

    def if_empty(self):
        if self.input.strip()== '':
            print("invalid input.Try again")
            return True
        return False

    def if_range(self):
        if not self.input.isdigit():
            print("Invalid input. Please Enter numbers")
            return True
        self.input=int(self.input)
        if not self.input in range(101):
            print("Make sure that your input doesnt exceed 100")
            return True
        return False   # FIXED

    def category_valid(self):
        if  self.input.lower() == 'fa' or  self.input.lower() == 'sa':
            return False
        else:
            print('Please Enter either "Sa"  or "Fa"')
            return True

    def maxi_Category(self,category):
        global SA_count, FA_count
        self.category=category
        self.input=int(self.input)

        if self.category == "FA":
            if FA_count + self.input > 60:   # FIXED
                print("ALL total FA weight should not exceed 60")
                return True
            else:
                return False

        elif self.category == "SA":
            if SA_count + self.input > 40:   # FIXED
                 print("ALL total SA weight should not exceed 40")
                 return True
            else:
                return False

    def if_target(self,category):
        global SA_count, FA_count
        self.category=category
        self.input=int(self.input)

        if self.category =='SA':
            if SA_count + self.input > 40:   # FIXED
                print("You have reached maximum Sa weight.")
                return True
            else:
                SA_count+=self.input

        if self.category == 'FA':
            if FA_count + self.input > 60:   # FIXED
                print("You have reached maximum Fa weight.")
                return True
            else:
                FA_count+=self.input

        return False

    def conditionalExit(self):
        global  SA_count, FA_count
        if FA_count != 60:
            scale = 60- FA_count
            print("Please Make sure That all the FA weight is 60 ")
            print(f"Remaining FA Weight = {scale}")
            return True

        if SA_count != 40:
            scale = 40 - SA_count
            print("Please Make sure That all the SA weight is 40 ")
            print(f"Remaining SA Weight = {scale}")
            return True

        return False



class Calculation_Logic():
    def __init__(self,input,weight,category):
        self.input=input
        self.weight=weight
        self.category=category          

    def weighted_grade(self):
        real_weight=(self.input/100)*self.weight
        if self.category.lower() == 'fa':
            Fa_real_weight.append(real_weight)
        if self.category.lower()== 'sa':
            Sa_real_weight.append(real_weight)

    def resummissions(self):
        Fail_list=[]
        highest_weight= 0
        for g in range(len(FA_names)):
            grades = FA_Grades[g]
            weight= FA_weight[g]
            name = FA_names[g]
            if grades < 50 :
                if weight > highest_weight:
                    highest_weight = weight
                    Fail_list = [name]
                elif weight == highest_weight:
                    Fail_list.append(name)
        return ",".join(Fail_list)
        
        
    def calculating_Gpa(self):
        Total_FA = sum(Fa_real_weight)
        Total_SA = sum(Sa_real_weight)
        Total_Grade = Total_FA+Total_SA
        Final_GPA = (Total_Grade/100)*5.0

        resub= self.resummissions()
        if not resub :
            resub = 'None'

        if Total_FA >= 30 and Total_SA >= 20:
            status = 'Pass'
        else:
            status = 'Fail'

        Results=f"""
--------RESULTS-----------
Total Formative:    {Total_FA}/60
Total Summative:    {Total_SA}/40
--------------------------
Total Grade:        {Total_Grade}/100
GPA:                {Final_GPA}
Status:             {status}
Resubmission:       {resub}  
"""

        print(Results)



class csv_preparation():
    def save(self):   # FIXED - moved code into a method
        Dictionary_list=[]

        for g in range(len(FA_names)):
            name= FA_names[g]
            weight= FA_weight[g]
            category = 'FA'
            grades=FA_Grades[g]
            results = {
                'Assignment': name,
                'Category': category,
                'Grade': grades,
                'Weight': weight,    
            }
            Dictionary_list.append(results)

        for g in range(len(SA_Names)):
            name= SA_Names[g]
            weight= SA_weight[g]
            category = 'SA'
            grades=SA_Grades[g]
            results = {
                'Assignment': name,
                'Category': category,
                'Grade': grades,
                'Weight': weight,    
            }
            Dictionary_list.append(results)

        titles=['Assignment','Category','Grade','Weight']

        with open('grades.csv', mode='w', newline='') as file:   # FIXED (new file)
            writer =csv.DictWriter(file, fieldnames=titles)
            writer.writeheader()
            writer.writerows(Dictionary_list)

        print("Details added to grades.csv successfully")



welcome="""
====================================================
WELCOME TO GRADE CALCULATOR! CLICK NEXT TO CONTINUE.
====================================================
"""
print(welcome)
while True:
    Name=input("Enter assignment name: ")
    name=validation(Name)
    if name.if_empty():
         continue

    while True:
        category=input("Enter Category: ")
        Category=validation(category)

        if  Category.if_empty(): 
            continue
        if Category.category_valid():
            continue

        if category.lower() == 'fa':
            if FA_count == 60:
                print("You have reach maximum FA weight. Please try another ")
                continue
            else:
                category= "FA"

        if category.lower() == 'sa':
            if SA_count == 40:
                print("You have reach maximum SA weight. Please try another")
                continue
            else:
                category= "SA"

        break

    while True:
        marks=input("Enter Grade Obtained: ")
        Grades=validation(marks)

        if Grades.if_empty(): 
            continue
        if Grades.if_range():
            continue

        marks=int(marks)

        if category == "FA":
            if FA_count == 60:
                print("You are not allowed to add more FA")
                continue
            else:
                FA_Grades.append(marks)

        elif category == "SA":
            if SA_count == 40:
                print("You are not allowed to add more SA")
                continue
            else:
                SA_Grades.append(marks)

        break


    while True: 
        Weight=input("Enter assinment Weight: ")
        size=validation(Weight)
        
        if size.if_empty(): 
            continue
        if size.if_range():
            continue
        if size.maxi_Category(category):
            continue
        if size.if_target(category):
            continue

        Weight=int(Weight)

        if category.lower() == 'fa':
            FA_weight.append(Weight)
            FA_names.append(Name)

        if category.lower() =='sa':
            SA_weight.append(Weight)
            SA_Names.append(Name)

        break


    Results = Calculation_Logic(marks, Weight, category)
    Results.weighted_grade()

    if FA_count == 60 and SA_count == 40:
        break

    while True:
        Answer=input("Do you want to Add another assignment? (y/n): ")
        if Answer.strip() == '': 
            print("invalid input.Try again")
            continue
        if Answer.lower() == 'y':
            break   
        elif Answer.lower() == 'n':
            size.conditionalExit()
            continue
        else:
            print("Please enter either 'y' or 'n'")
            continue

end_message="""
================================================================================
CONGRATULATIONS!!! ALL YOUR GRADES HAVE BEEN CALCULATED! PLEASE FIND THEM BELOW.
================================================================================
"""
print(end_message)
# FINAL RESULTS
Results.calculating_Gpa()

# SAVE CSV
csv_preparation().save()