#Minute rate in interval <8:00:00,16:00:00) is 1 CZK for each started minute. Otherwise, it is 0,50 CZK. Appropriate rate is chosen for each minute of a call
#For calls longer than 5 mins bonus rate 0,20 CZK is applied for all remaining minutes, no mater of a daytime.
#Keep most frequent number out of charge (free), if there is more than one number, take the one with arithmetically higher number
import datetime,statistics,csv
dcr=1.0;ncr=0.5;dis=0.2;t1=' 08:00'; t2=' 16:00';  
 
def Get_most_frequent(List):
    list1=statistics.multimode(List)
    return list1

def Apply_promo_offer(phno_list,bill_list):
    freqno_list=Get_most_frequent(phno_list)
    freqno_bill=[];promo=[]
    for i in range(len(freqno_list)):
        freqno_bill.append(0.0)
        for j in range(len(phno_list)):
            if freqno_list[i]==phno_list[j]:
                freqno_bill[i]=float(freqno_bill[i])+float(bill_list[j])
    maspos=freqno_bill.index(max(freqno_bill))
    promono=freqno_list[maspos]
    for i in range(len(phno_list)):
        if phno_list[i]==promono:
            bill_list[i]=0.0
    promo=[promono, max(freqno_bill)] 
    return promo     

def Getbill(dtobjs,caseid):
#Case1: Day time, Case2: Started in day and end in night, Case3: Started in Night and ended in day, Case4: Night time       
    startdtobj=dtobjs[0]
    enddtobj  =dtobjs[1]
    dtobj8  =dtobjs[2]
    dtobj16  =dtobjs[3]
    calldur = (enddtobj-startdtobj).total_seconds() / 60  
    if caseid == 1:
        bill=calldur*dcr
    elif caseid == 2:
        ddur=(dtobj16-startdtobj).total_seconds() / 60
        bill=ddur*dcr+(calldur-ddur)*ncr
    elif caseid == 3:
        ndur=(dtobj8-startdtobj).total_seconds() / 60
        bill=ndur*ncr+(calldur-ndur)*dcr
    elif caseid == 4:
        bill=calldur*ncr
    if calldur>5:
        bill=bill-(calldur-5)*dis
    return bill

def readcsvfile(fname):
    f=open(fname,'r', encoding='UTF8')
    csv_reader = csv.reader(f)
    i=0;inplist=[]
    for line in csv_reader:
        str0=line[0] + ',' + line[1] + ',' + line[2]
        inplist.append(str0)
        i=i+1
    print(f'NOTE: There are total {i} call record present in the file')
    f.close
    return inplist
def main():
    fname='generated_sample_2.csv'
    inplist=[]; phno_list=[]; dur_list=[]; bill_list=[]
    inplist=readcsvfile(fname)
    for ln in inplist:
        str0=ln
        inp=str0.split(',')
        phno_list.append(inp[0])
        str1=inp[1].split()
        startdtobj=datetime.datetime.strptime(inp[1], '%m/%d/%Y %H:%M')
        enddtobj  =datetime.datetime.strptime(inp[2], '%m/%d/%Y %H:%M')
        dtobj8  =datetime.datetime.strptime(str1[0] + ' 08:00', '%m/%d/%Y %H:%M')
        dtobj16  =datetime.datetime.strptime(str1[0] + ' 16:00', '%m/%d/%Y %H:%M')
        dtobjs=[startdtobj,enddtobj,dtobj8,dtobj16]
        calldur = (enddtobj-startdtobj).total_seconds() / 60
        bill=0.0
        if (startdtobj.time() >= dtobj8.time()) and (startdtobj.time() <= dtobj16.time()):
            if (enddtobj.time() >= dtobj8.time()) and (enddtobj.time() <=dtobj16.time()):
                caseid=1
                bill=Getbill(dtobjs,caseid)           
            else:
                caseid=2         
                bill=Getbill(dtobjs,caseid)
        else:
            if (enddtobj.time() > dtobj8.time()) and (enddtobj.time() < dtobj16.time()):
                caseid=3
                bill=Getbill(dtobjs,caseid)         
            else:
                caseid=4          
                bill=Getbill(dtobjs,caseid)
        dur_list.append(calldur)
        bill_list.append(bill)
    print(f'Total bill before Promotional offer: {sum(bill_list)} CZK')
    promo=Apply_promo_offer(phno_list,bill_list)
    print(f'Total bill after Promotional offer: {sum(bill_list)} CZK')
    print(f'Promotional offer has been given to the customer: {promo[0]} of amount: {promo[1]} CZK')
    #print(dur_list,'\n',bill_list)

if __name__ == "__main__":
    main()
