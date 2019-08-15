import requests, json
import datetime, time
import re



def getLiveStatus(trainNo):
    try:
        # baseUrl = "https://api.railwayapi.com/v2/live/train/"
        baseUrl ="https://www.confirmtkt.com/train-running-status/"
        #date = datetime.date.today()
        #url = baseUrl+trainNo+"/date/"+date.strftime("%m-%d-%Y")+"/apikey/"+"v_j_t_0_1_f_f_u_n_o"
        url = baseUrl+trainNo

        response_obj = requests.get(url)
        #print(response_obj.content)
        #result = response_obj.json()

        if response_obj.status_code == 200:
            result = response_obj.text.split("circle blink")[1].split("</span")[0].split(">")[-1:]
            print(result[0])
            return result[0]
        
        else : 
             return "None" 
    
    except Exception as e:

        return "Some Error Occurred while getting train status"


def getTrainName(trainName,source):
    try:
        cur_time =  int(round(time.time() * 1000))
        url = "https://search.railyatri.in/mobile/trainsearch?callback=jQuery112002057801848788252_1565858562042&q="+trainName+"&slip_type=1&_="+str(cur_time)

        response_obj = requests.get(url)

        trains = response_obj.text
        lists = trains.split("[")

        for l in lists:
            if source.upper()+" -" in l:
                return re.sub("[^0-9]","",l)
    except Exception as e:
       return "Some Error Occurred while fetching train number"

#if __name__ == "__main__":    
#     trainNo = getTrainName("Brindavan Express","Bangalore")
#      getLiveStatus(trainNo)
