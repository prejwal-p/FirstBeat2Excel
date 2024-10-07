import pymupdf
import pandas as pd

def extract_third_page_data(text):
    # Extracting the data from the second page
    
    ###################### Search Strings ######################
        
    vo2_max_value_ss = "Your V02max result is"
    vo2_max_status_ss = "fitness level result is"
    age_ss = "Age"
    height_ss = "Height"
    weight_ss = "Weight"
    bmi_ss = "Body mass index"
    resting_hr_ss = "Resting heart rate"
    max_hr_ss = "Max. heart rate"
    day_data_indices = []

    vo2_max = None
    vo2_max_status = None
    age = None
    height = None
    weight = None
    bmi = None
    resting_hr = None
    max_hr = None
    about_measurement_start = None
    about_measurement_end = None


    # Searching which element of list contains the search string
    for i in range(len(text)):
        if vo2_max_value_ss.lower() in text[i].lower():
            vo2_max = text[i].split(vo2_max_value_ss)[1].split(' ')[1]

        if vo2_max_status_ss.lower() in text[i].lower():
            vo2_max_status = text[i].split(vo2_max_status_ss)[1].split(' ')[1]

        # Find the start and end of the "About Measurement" section of the report
        if "ABOUT MEASUREMENT" in text[i]:
            about_measurement_start = i
        
        if "Report ID" in text[i]:
            about_measurement_end = i
        
        # CHeck if the vaiable is a day of the week Ex. Monday, Tuesday, etc. This is used to more granular data extraction
        if text[i].lower() in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            day_data_indices.append(i)

    about_data = text[about_measurement_start:about_measurement_end]

    for i in range(len(about_data)):
        if age_ss.lower() in about_data[i].lower():
            if age is None:
                age = about_data[i+1]

        if height_ss.lower() in about_data[i].lower():
            if height is None:
                height = about_data[i+1]
        
        if weight_ss.lower() in about_data[i].lower():
            if weight is None:
                weight = about_data[i+1]

        if bmi_ss.lower() in about_data[i].lower():
            if bmi is None:
                bmi = about_data[i+1]

        if resting_hr_ss.lower() in about_data[i].lower():
            if resting_hr is None:
                resting_hr = about_data[i+1]

        if max_hr_ss.lower() in about_data[i].lower():
            if max_hr is None:
                max_hr = about_data[i+1]

    data = {
        "VO2 Max": vo2_max,
        "VO2 Max Status": vo2_max_status,
        "Age": age,
        "Height": height,
        "Weight": weight,
        "BMI": bmi,
        "Resting HR": resting_hr,
        "Max HR": max_hr
    }

    for counter, idx in enumerate(day_data_indices):
        if counter == len(day_data_indices)-1:
            day_data = text[idx:]
        else:
            day_data = text[idx:day_data_indices[counter+1]]

        day = day_data[0]
        date_str = day_data[1]
        start_time_str = day_data[2].strip("Start time ")
        duration_str = day_data[3].strip("Duration ")
        hr_range = day_data[5].split(" / ")
        hr_low = hr_range[0]
        hr_avg = hr_range[1]
        hr_high = hr_range[2]
        additional_info = day_data[6:]

        data[f"Day_{counter+1} Day"] = [day]
        data[f"Day_{counter+1} Date"] = [date_str]
        data[f"Day_{counter+1} Start Time"] = [start_time_str]
        data[f"Day_{counter+1} Duration"] = [duration_str]
        data[f"Day_{counter+1} HR Low"] = [hr_low]
        data[f"Day_{counter+1} HR Avg"] = [hr_avg]
        data[f"Day_{counter+1} HR High"] = [hr_high]
        data[f"Day_{counter+1} Additional Info"] = [additional_info]

    return pd.DataFrame(data)


def extract_first_page_data(text):
    overall_score = text[2]
    overall_score_status = text[4]
    stress_and_recovery_balance = text[11].split("/")[0]
    restorative_effect_of_sleep = text[13].split("/")[0]
    physical_activity = text[15].split("/")[0]
    
    data = {
        "Overall Score": overall_score,
        "Overall Score Status": overall_score_status,
        "Recovery Score": stress_and_recovery_balance,
        "Sleep Score": restorative_effect_of_sleep,
        "Physical Activity Score": physical_activity
    }

    return pd.DataFrame(data, index=[0])
