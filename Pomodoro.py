import discord  # importing the discord library
from time import *  # importing all functions from time library

TOKEN = 'NzY5ODc2MDMyNTQxOTUwMDAy.X5VY7Q.b_isOFWa_5hiOxA1-gJemoOuWSk'  # storing the bot's unique id in variable TOKEN
client = discord.Client()  # Creates a client to communicate with the discord server


# Function that operates the Pomodoro timer
async def timer(cycle, message):
    seconds = time()  # Variable seconds stores the time at the start of the function execution
    i = 1  # variable that stores the number of cycles completed
    j = 1  # variable that stores the number of study sessions completed
    flag = 0  # flag variable that signifies whether study session is running or break is running
    while 1:  # Infinite Loop until Study Cycles Remain
        if i >= cycle + 1:  # checks if all the assigned cycles are complete
            break  # If cycles are complete, break the loop
        await message.channel.send(
            "Start of Cycle -> " + str(i))  # If Cycles Remain, send message on discord of starting cycle
        await message.channel.send('Start Studying')  # Send Message to start studying
        while 1:  # Infinite loop until 4 study sessions of the cycle are complete
            seconds1 = time()  # variable seconds1 stores the time at the start of every iteration
            if j < 4 and seconds1 - seconds >= 25 and flag == 0:  # if sessions remain and seconds1 has crossed 25 minutes and if flag = 0 (Study Session)
                await message.channel.send("5 minutes break")  # Prints 5 minute break in the server channel
                seconds = seconds1  # Updating the seconds variable to current time to start the break
                j += 1  # Incrementing sessions by 1
                flag = 1  # Marking flag as 1 since break has started
                continue  # Skip to next iteration
            if j <= 4 and seconds1 - seconds >= 5 and flag == 1:  # if sessions remain and seconds1 has crossed 5 minutes and if flag = 1 (Break Session)
                await message.channel.send("Break's Over, Start Studying")  # Prints Break's Over in the server channel
                seconds = seconds1  # Updating the seconds variable to current time to start the Study Session
                flag = 0  # Marking flag as 0 since Study Session has started
                continue  # Skip to next iteration
            if j == 4 and i == cycle and seconds1 - seconds >= 25:  # If the study session is equal to 4 and all the cycles are complete and the study time is up
                await message.channel.send(
                    "Study Cycle Complete!")  # Prints that the Study Cycle is Complete in the server channel
                i += 1  # Incrementing Cycles by 1
                break  # terminates the loop

            if j == 4 and i != cycle and seconds1 - seconds >= 25 and flag == 0:  # If the study session is equal to 4 but all the cycles are not complete and the study time is up
                await message.channel.send(
                    f"Cycle {i} Complete! Time for a 30 minutes break")  # Prints that this Study Cycle is Complete, and there's a 30 minute break before the next cycle starts in the server channel
                seconds = seconds1  # Updating the seconds variable to current time to start the whole cycle's Break Session
                j += 1  # Incrementing sessions by 1
                flag = 1  # Marking flag as 1 since break has started
                continue  # Skip to next iteration

            if j >= 4 and i != cycle and seconds1 - seconds >= 30 and flag == 1:  # If the study session is completed but all the cycles are not complete and the cycle interval time is up
                await message.channel.send(
                    "Breaks Over, Start Studying for new Cycle")  # Prints Break's Over in the server channel
                j = 1  # initialize j to 1
                i += 1  # increment i
                flag = 0  # Marking flag as 0 since Study Session has started
                break  # breaking current cycle


@client.event  # When the client receives any event from the server, it works out which function to call and calls that function
async def on_message(message):  # Event triggered when a new message is received in the server
    msg = message.content.lower()  # Variable msg stores the contents of the message sent by the user, in lowercase
    user = str(message.author)[:len(str(
        message.author)) - 5]  # Variable user stores the username of the user by slicing off the last 5 characters that contain the unique id of each user

    if message.author == client.user:  # This prevents the bot from responding to itself
        return
    if msg == 'hi' or msg == 'hello':  # Programming the bot to respond to a greeting from the user
        await message.channel.send('Hello ' + user)  # Greets the person who saod hello or hi
    elif msg.startswith('-'):  # Programming the bot to take commands from the user
        msg = msg[1:]  # Slicing off the command prefix
        if msg.startswith('start'):  # Calling the timer function if the user wishes to start the timer
            l = msg.split(' ')  # Reading the second part of the command and storing it in the number of cycles
            if len(l) > 1 and l[1].isnumeric():  # Checking if the number of cycles entered entered and it is a number
                cycle = int(l[1])  # Reading the number of Cycles
                await timer(cycle, message)  # Calling the timer function
                return

            await message.channel.send('Sorry, ' + user + '. That was an invalid input.')  # Failure message block
            await message.channel.send('The correct format is   -start number_of_cycles')
            await message.channel.send('Type \'-help\' to see a list of valid commands.')

        if msg == 'help':  # Adding a help block so the user can understand the commands
            await message.channel.send('Welcome to Pomodoro Study Assistant. Enhance your learning\n\n')
            await message.channel.send('--------------------------------------')
            await message.channel.send('--> Here are a list of commands you can use :')
            await message.channel.send('-start number_of_cycles\t: To start your Study Cycle')
            await message.channel.send('-help\t\t: To see a list of valid Commands')


client.run(TOKEN)  # Starting the bot in the server
