import nextcord, os.path, json, datetime
from nextcord.ext import commands, tasks
from datetime import datetime

class hostTools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.database2 = {'notifications' : {}}
        self.database3 = {'hostRoster' : {}}
        self.roster_category = None

    def cog_unload(self):
        self.sendNotification.cancel()
        self.updateHostSlots.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        # Set global variable for channels
        # Because of the funny icons in Dogegs we have to use the ID of the channel 451858500784619550
        # Because of the funny icons in Monkeys we have to use the ID of the channel 911066596456415269
        global botCommandsChannel 
        global dogegsChannel
        global hostNotificationsChannel
        global hostSchedulingChannel
        botCommandsChannel = nextcord.utils.get(self.client.get_all_channels(), name=f"bot-commands")
        dogegsChannel = nextcord.utils.get(self.client.get_all_channels(), id=451858500784619550)
        hostNotificationsChannel = nextcord.utils.get(self.client.get_all_channels(), name=f"host-notifications")
        hostSchedulingChannel = nextcord.utils.get(self.client.get_all_channels(), name=f"scheduling")
        #Check and load pre-existing roster JSON
        if os.path.exists('autoSlot.json'):
            with open('autoSlot.json', 'r') as json_file:
                self.database = self.client.get_cog('autoSlot').database
        if os.path.exists('autoNotifications.json'):
            with open('autoNotifications.json', 'r') as json_file2:
                self.database2 = json.load(json_file2)
        if os.path.exists('hostRoster.json'):
            with open('hostRoster.json', 'r') as json_file3:
                self.database3 = json.load(json_file3)
        self.sendNotification.start()
        self.updateHostSlots.start()


    @commands.command(name = "addEvent", help = "Adds a discord event for a specific operation")
    async def addEvent(self, ctx, operation_id):

        ''' 
        Created 1-18-2024 by Chief
        Updated 1-22-2024 by Chief

        -- Purpose -- 
        * Create a discord event for Arma Operations
        
        -- Logic -- 
        * Grab and Format all inputs
        * Check if the event already exists
        * Create event using nextcord's ctx.guild.create_scheduled_event()
        * Send notification
        
        -- Error Prevention -- 
        * Validate operation ID is valid
        * Prevent event creation if event already exists
        '''

        # Check if operation ID exists
        if await checkOpID(self, operation_id) is not None: return
        
        # Grab variables required to create the scheduled event
        nameInput=f"{self.database['operations'][operation_id]['name']}"
        entity_typeInput = nextcord.ScheduledEventEntityType.voice
        start_timeInput = datetime.utcfromtimestamp(int(self.database['operations'][operation_id]['operation_timestamp']))
        channelInput = dogegsChannel
        end_timeInput = datetime.utcfromtimestamp(int(self.database['operations'][operation_id]['operation_timestamp']) + 7200)

        # Check if start time is in the past as it will fail to complete if it is
        if await checkIfTimeIsInThePast(start_timeInput) is not None: return

        # Generate discord event using pre-defined variables if event with same name doesnt exist
        if (await eventExists(ctx, nameInput)): 
            await botCommandsChannel.send("Event for " + nameInput + " already exists")
        else: 
            await ctx.guild.create_scheduled_event(name = nameInput, entity_type = entity_typeInput, start_time = start_timeInput, channel = channelInput, end_time = end_timeInput, description = nameInput)
            await botCommandsChannel.send("Event " + nameInput + " created")

        

    @commands.command(name = "addReminder", help = "Schedule a reminder to ping an @")
    async def addReminder(self, ctx, user, notifTime, notifMessage = None, operation_id = None):
        
        ''' 
        Created 1-19-2024 by Chief
        Updated 2-25-2024 by Chief

        -- Purpose -- 
        * Create a reminder to ping Arma Operation Hosts at specific times

        -- Logic -- 
        * Loop through a json file containing the notifications every minute using nextcord's @tasks.loop(seconds = 60.0)
        * If the notification time of the file is greater than the current time, send the notification and delete the entry
        * Else proceed to next entry

        -- Json File Format --
        Notification Timestamp (In Unix Seconds), Member_ID to ping, Notification Message, Operation ID (If applicable)

        -- Error Prevention -- 
        * Validate User Input
        * If json does not exist create a new one
        '''

        # Check if operation ID exists, ignore if the operation ID input is null
        if (operation_id is not None) and (await checkOpID(self, operation_id) is not None): return

        # Check if user exists
        if await checkIfUserExists(ctx, user) is not None: return

        # Validate input is a number
        if await checkIfIntNumber(notifTime) is not None: return

        # Loop through json and find the lowest value notification ID available
        notificationID = 1
        while notificationID < 1000:
            if str(notificationID) not in self.database2['notifications'] :
                break
            else:
                notificationID += 1

        # Add row to json with input data and save the file
        self.database2['notifications'].update({str(notificationID) : {'User': user, 'Time': notifTime, 'Message': notifMessage, 'Operation ID': operation_id}})
        saveNotifJsonData(self)
        formattedTime = "<t:" + str(notifTime) + ":F>"
        if (operation_id is not None):
            await hostNotificationsChannel.send(f"Notification created for {user} at {formattedTime} with message \"{notifMessage}\" for operation ID {operation_id}")
        else:
            await botCommandsChannel.send(f"Notification created for {user} at {formattedTime} with message \"{notifMessage}\"")

        
    @commands.command(name = "deleteReminder", help = "Delete a reminder")
    async def deleteReminder(self, ctx, notificationID: str):
        ''' 
        Created 1-21-2024 by Chief
        Updated 1-22-2024 by Chief

        -- Purpose -- 
        * Delete a specific reminder from the autoNotifications json

        -- Logic -- 
        * Grab data from the json before the data is deleted
        * Based on the user input for notification ID, delete that specific entry
        * Send deletion notification message
        '''

        # Validate input is a number
        if await checkIfIntNumber(notificationID) is not None: return

        # Grab data from message before deletion
        messageToSend = f"Notification created for {self.database2['notifications'][notificationID]['User']} at {self.database2['notifications'][notificationID]['Time']} removed"

        # Delete value from internal DB
        del self.database2['notifications'][notificationID]
        saveNotifJsonData(self)
        await botCommandsChannel.send(messageToSend)


    @commands.command(name = "listReminders", help = "List Reminders")
    async def listReminders(self, ctx):
        ''' 
        Created 1-21-2024 by Chief
        Updated 1-22-2024 by Chief

        -- Purpose -- 
        * List all the reminders stored in the autoNotifications json

        -- Logic -- 
        * Looping through the json
        * Format the time in the long discord time format
        * Send notification to bots channel
        '''
        notifListEmbedData = ""
        print("Attempting Reminder List")
        # Loop through notification DB and send the list to the bots command channel
        for notificationID in self.database2['notifications'].copy():
            user = ctx.guild.get_member(int(self.database2['notifications'][notificationID]['User'].translate({ord(i): None for i in '@<>'})))
            time = "<t:" + str(self.database2['notifications'][notificationID]['Time']) + ":F>\n"
            notifListEmbedData = notifListEmbedData + f"{user} {time}"
            #await botCommandsChannel.send(f"Notification {notificationID}: {user} {time} {self.database2['notifications'][notificationID]['Message']}")
        notifListEmbed = nextcord.Embed(title=f"Active Notifications", description=notifListEmbedData, color=0x0E8643)
        await botCommandsChannel.send(embed=notifListEmbed)


    @commands.command(name = "hostSlot", help = "Signup for host timeslot")
    async def hostSlot(self, ctx, slot_id):

        # Check to see if the imbed already exists
        scheduler_message = await hostSchedulingChannel.history().get(author__id = self.client.user.id)

        hostJsonData = self.database3['hostRoster'].copy()

        # Check if slot exists
        if hostJsonData.get(slot_id) == None:
            return await botCommandsChannel.send(f"Host Slot ID {slot_id} not found.")
        
        # Check if slot already has user
        if self.database3['hostRoster'][slot_id]["User"] != "":
            return await botCommandsChannel.send("Please remove the person from this slot before trying to claim it.")
        
        #Assign Slot
        self.database3['hostRoster'][slot_id]["User"] = ctx.author.mention

        embedData = await hostJsonEmbedData(self)
        saveHostRosterJsonData(self)
        
        if (scheduler_message == None):
            hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
            await hostSchedulingChannel.send(embed=hostEmbed)
        else:
            hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
            await scheduler_message.edit(embed=hostEmbed)

        bChannel = await botCommandsChannel.send("About to be edited.")
        await bChannel.edit(f"{ctx.author.mention} has added themself to Host Slot {slot_id}")
        
        
    @commands.command(name = "removeHostSlot", help = "Remove signup for host timeslot")
    async def removeHostSlot(self, ctx, slot_id):

        # Check to see if the imbed already exists
        scheduler_message = await hostSchedulingChannel.history().get(author__id = self.client.user.id)

        hostJsonData = self.database3['hostRoster'].copy()

        # Check if slot exists
        if hostJsonData.get(slot_id) == None:
            return await botCommandsChannel.send(f"Host Slot ID {slot_id} not found.")
        
        if self.database3['hostRoster'][slot_id]["User"] != ctx.author.id:
            if "Campaign Host" in ctx.author.roles or "Operations Command" in ctx.author.roles or "Command Consultant" in ctx.author.roles or "Operation Host" in ctx.author.roles:
                return await botCommandsChannel.send('You are not a host. Only hosts can remove another operative from a slot.')
            self.database3['hostRoster'][slot_id]["User"] = ""
        else:
            self.database3['hostRoster'][slot_id]["User"] = ""
        embedData = await hostJsonEmbedData(self)
        saveHostRosterJsonData(self)
        
        if (scheduler_message == None):
            hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
            await hostSchedulingChannel.send(embed=hostEmbed)
        else:
            hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
            await scheduler_message.edit(embed=hostEmbed)

        bChannel = await botCommandsChannel.send("About to be edited.")
        await bChannel.edit(f"{ctx.author.mention} has removed themself from Host Slot {slot_id}")
    '''
    @commands.command(name = "test", help = "test")
    async def test(self, ctx):
        data = await nextSeveralDaysOfTheWeek(5,12)
        commandData = ""
        hostJsonData = self.database3['hostRoster'].copy()
        count = 0
        print("This is the data")
        print(hostJsonData)
        if hostJsonData == {}:
            print("It Empty bro")
            for i in data:
                print(i)
                count = count + 1
                self.database3['hostRoster'].update({str(count) : {'Time': data[count-1], 'User': ""}})
        saveHostRosterJsonData(self)
        hostJsonData = self.database3['hostRoster'].copy()
        print("This is the data2")
        print(hostJsonData)
        for i in data:
            print(i)
            commandData = commandData + f"<t:{i}:D>\n"
        embedData = await hostJsonEmbedData(self)
        await botCommandsChannel.send("commandData")
        await botCommandsChannel.send(commandData)
        await botCommandsChannel.send("embedData")
        await botCommandsChannel.send(embedData)

    @commands.command(name = "test2", help = "test")
    async def test2(self, ctx):
        # Check to see if the embed already exists
        scheduler_message = await hostSchedulingChannel.history().get(author__id = self.client.user.id)
        data = await nextSeveralDaysOfTheWeek(5,12)
        hostJsonData = self.database3['hostRoster'].copy()
        currentUTCTimePlusOneDay = datetime.utcnow().timestamp() + 60000
        if hostJsonData == {}:
            for i in data:
                count = count + 1
                self.database3['hostRoster'].update({str(count) : {'Time': data[count-1], 'User': ""}})
        if int(self.database3['hostRoster'][str(1)]["Time"]) < currentUTCTimePlusOneDay:
            hostJsonData = self.database3['hostRoster'].copy()
            for i in hostJsonData:
                if int(i) == len(hostJsonData):
                    break
                self.database3['hostRoster'][str(i)]["Time"] = self.database3['hostRoster'][str(int(i)+1)]["Time"]
            self.database3['hostRoster'][str(len(hostJsonData))]["Time"] = data[11]
            self.database3['hostRoster'][str(len(hostJsonData))]["User"] = ""
            embedData = await hostJsonEmbedData(self)
            if (scheduler_message == None):
                hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
                await hostSchedulingChannel.send(embed=hostEmbed)
            else:
                hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
                await scheduler_message.edit(embed=hostEmbed)
        '''

    @tasks.loop(seconds=60)
    async def sendNotification(self):
        ''' 
        Created 1-21-2024 by Chief
        Updated 1-22-2024 by Chief

        -- Purpose -- 
        * Send notifications for pre-defined reminders

        -- Logic -- 
        * Every 60 seconds go through the autoNotifications json
        * If the notification time is less than the current time, send notification and delete the entry
        '''
        currentUTCTime = datetime.utcnow()
        # Every 60 seconds loop through the notification DB by creating a temp copy of the DB and comparing the timestamp of the current time to the time in the DB
        for notificationID in self.database2['notifications'].copy():
            if datetime.utcfromtimestamp(int(self.database2['notifications'][notificationID]['Time'])) < currentUTCTime:
                if (self.database2['notifications'][notificationID]['Operation ID'] is not None):
                    await hostNotificationsChannel.send(f"{self.database2['notifications'][notificationID]['User']} {self.database2['notifications'][notificationID]['Message']}")
                else:
                    await botCommandsChannel.send(f"{self.database2['notifications'][notificationID]['User']} {self.database2['notifications'][notificationID]['Message']}")
                del self.database2['notifications'][notificationID]
                saveNotifJsonData(self)
                
    @tasks.loop(seconds=3600)
    async def updateHostSlots(self):
        scheduler_message = await hostSchedulingChannel.history().get(author__id = self.client.user.id)
        currentUTCTimePlusOneDay = datetime.utcnow().timestamp() + 60000
        hostJsonData = self.database3['hostRoster'].copy()
        # Check to see if the host json exists
        if hostJsonData == {}:
            count = 0
            data = await nextSeveralDaysOfTheWeek(5,12)
            for i in data:
                count = count + 1
                self.database3['hostRoster'].update({str(count) : {'Time': data[count-1], 'User': ""}})
            saveHostRosterJsonData(self)
            embedData = await hostJsonEmbedData(self)
            if (scheduler_message == None):
                hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
                await hostSchedulingChannel.send(embed=hostEmbed)
            else:
                hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
                await scheduler_message.edit(embed=hostEmbed)
        
        # If the earliest slot in the host roster is earlier than the current day + 1 than remove it, push all dates up, and 
        if int(self.database3['hostRoster'][str(1)]["Time"]) < currentUTCTimePlusOneDay:
            scheduler_message = await hostSchedulingChannel.history().get(author__id = self.client.user.id)
            hostJsonData = self.database3['hostRoster'].copy()
            data = await nextSeveralDaysOfTheWeek(5,12)
            for i in hostJsonData:
                if int(i) == len(hostJsonData):
                    break
                self.database3['hostRoster'][str(i)]["Time"] = self.database3['hostRoster'][str(int(i)+1)]["Time"]
                self.database3['hostRoster'][str(i)]["User"] = self.database3['hostRoster'][str(int(i)+1)]["User"]
            self.database3['hostRoster'][str(len(hostJsonData))]["Time"] = data[11]
            self.database3['hostRoster'][str(len(hostJsonData))]["User"] = ""
            saveHostRosterJsonData(self)
            embedData = await hostJsonEmbedData(self)
            if (scheduler_message == None):
                hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
                await hostSchedulingChannel.send(embed=hostEmbed)
            else:
                hostEmbed = nextcord.Embed(title=f"Host Scheduler", description=embedData, color=0x0E8643)
                await scheduler_message.edit(embed=hostEmbed)

    # Required for sendNotification loop
    @sendNotification.before_loop
    async def beforeSendNotification(self):
        await self.client.wait_until_ready()
    
    @sendNotification.before_loop
    async def beforeUpdateHostSlots(self):
        await self.client.wait_until_ready()

# Functions
def saveNotifJsonData(self):
    # Dumps data to autoNotifications.json
    with open('autoNotifications.json', 'w') as f:
        json.dump(self.database2, f)

def saveHostRosterJsonData(self):
    # Dumps data to autoSlot.json
    with open('hostRoster.json', 'w') as f:
        json.dump(self.database3, f)

async def eventExists(ctx, nameInput):
    # Loop through active events and if the name of the event is identical to the name of the operation, return True
    async for event in ctx.guild.fetch_scheduled_events():
        if (event.name == nameInput):
            return True
        else:
            False

async def checkIfUserExists(ctx, userToVerify):
    # If the input is not a valid user, return message
    try:
        print(f"Verified user with ID {userToVerify}")
        ctx.guild.get_member(int(userToVerify.translate({ord(i): None for i in '@!<>'})))
    except:
        print(f"Failed to find user with id {userToVerify}")
        return await botCommandsChannel.send(f"{userToVerify} Invalid User, please make sure its an @User mention")
    return None

async def checkIfIntNumber(numberToVerify):
    # If the input is not a number, return message
    try:
        print(f"{numberToVerify} is an int")
        val = int(numberToVerify)
    except:
        print(f"Value failed to verify as an int {numberToVerify}")
        return await botCommandsChannel.send(f"{numberToVerify} Invalid Number, please make sure its a whole number")
    return None

async def checkOpID(self, operation_id):
    # If operation with this ID does not exist, return message
    try:
        print(f"{operation_id} is an operation")
        if operation_id not in self.database['operations']:
            return await botCommandsChannel.send("There is no operation present in the database with this ID.")
    except:
        print(f"Value failed to verify as an operation ID {operation_id}")
        return await botCommandsChannel.send("A problem occured with the operation id.")
    return None

async def checkIfTimeIsInThePast(inputTime):
    # If operation with this ID does not exist, return message
    currentTime = datetime.utcnow()
    if (currentTime > inputTime):
        print(f"Time found to be in the past current Time = {currentTime}, input Time = {inputTime}")
        return await botCommandsChannel.send(f"{inputTime} Is in the past, please make sure its greater than the current time {currentTime}")
    else:
        print(f"Input time is valid, current Time = {currentTime}, input Time = {inputTime}")
        return None
    
async def nextSeveralDaysOfTheWeek(dayOfWeek, numberOfThoseDays):
    currentUTCTime = datetime.utcnow()
    todayNumber = datetime.utcnow().weekday()
    if(dayOfWeek-todayNumber >= 0):
        daydifference = dayOfWeek-todayNumber
    else:
        daydifference = (7 + dayOfWeek - todayNumber)

    UNIXcurrentTimestamp = str(currentUTCTime.timestamp() - 18000)
    correctedCurrentTimestamp = int(UNIXcurrentTimestamp[0:10])
    upcomingDay = correctedCurrentTimestamp + (daydifference*86400)
    currentLoopTimestamp = upcomingDay
    dateList = []

    for i in range(numberOfThoseDays):
        dateList.append(currentLoopTimestamp)
        currentLoopTimestamp = currentLoopTimestamp + (7*86400)
    return dateList

async def hostJsonEmbedData(self):
    hostJsonData = self.database3['hostRoster'].copy()
    embedData = ""
    embedDataTime = ""
    embedDataUser = ""
    for i in hostJsonData:
        embedDataTime = self.database3['hostRoster'][i]["Time"]
        embedDataUser = self.database3['hostRoster'][i]["User"]
        if embedDataUser == "":
            x=1 
        else:
            embedDataUser = self.database3['hostRoster'][i]["User"]
        embedData = embedData + f"{i}: <t:{embedDataTime}:D> - {embedDataUser}\n"
    return embedData


async def deleteUserMessage(ctx):
    try:
        await ctx.message.delete()
    except:
        print()

async def silentPingSingleUser(inputMessage, user):
    await inputMessage.edit(user + " " + inputMessage.content)
    
def setup(client):
    client.add_cog(hostTools(client))