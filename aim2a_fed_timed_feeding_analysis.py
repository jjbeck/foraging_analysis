import glob
import pandas as pd
from pandas.core.tools.datetimes import to_time
import seaborn as sns
from datetime import datetime
from matplotlib import pyplot as plt
import time

def calculate_minutes(startDate, endDate):
    startHour = startDate.hour
    endHour = endDate.hour
    startMinute = startDate.minute
    endMinute = endDate.minute
    return abs((endHour - startHour)*60 + (endMinute - startMinute))


def cumul_intake(filePath):
    data = []
    for file in glob.glob(filePath+"*"):
        readCsv = pd.read_csv(file)
        dateString = readCsv["MM:DD:YYYY hh:mm:ss"][0]

        try:
            startDT = datetime.strptime(dateString, '%m/%d/%Y %H:%M:%S')
        except:
           
            startDT = datetime.strptime(dateString, '%m/%d/%Y %H:%M')

        fileName = file[file.rfind("/")+1:]
        fileName = fileName.replace(".CSV","")
        fileMetrics = fileName.split("_")
        
        id = fileMetrics[0]
        cnoCondition = fileMetrics[1]
        injection = fileMetrics[2]
        print(file)
       
        for ind in readCsv.index:
            try:
                minute_difference = calculate_minutes(datetime.strptime(readCsv["MM:DD:YYYY hh:mm:ss"][ind],'%m/%d/%Y %H:%M:%S') , startDT)
            except:
               minute_difference = calculate_minutes(datetime.strptime(readCsv["MM:DD:YYYY hh:mm:ss"][ind],'%m/%d/%Y %H:%M') , startDT)
            

            pelletIntake = readCsv["Pellet_Count"][ind]
            if minute_difference > 120:
                continue
            if minute_difference < 120 and ind == readCsv.count().Pellet_Count-1:
                for x in range(minute_difference, 120):
                    data.append([id, x, pelletIntake, cnoCondition, injection])
            else:
                data.append([id, minute_difference, pelletIntake, cnoCondition, injection ])
        
    df = pd.DataFrame(data, columns=['ID', 'Time Since Start', 'Pellet Intake', 'Injection Time', 'Injection'])
    groups = df.groupby("Injection")
    sem = groups.sem()
    print(sem)
    sns.lineplot(data=df, x='Time Since Start', y='Pellet Intake', hue='Injection', style='Injection Time')

    plt.show()

    
            



if __name__ == "__main__":
    cumul_intake("/home/jordan/Desktop/foragin_analysis_demo_data/")