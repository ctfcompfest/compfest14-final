const Discord = require(`discord.js`);
const client = new Discord.Client();

const flag = process.env.flag;

const responses = {
    neutral: [`Hi`, `Hey ho`, `Henlo`, `Hewwo`],
    lazy: [`I'm too lazy for this..`, `Yawnn`, `Is that all you've got?`, `Meh`],
    amazed: [`Wowie..`]
};

const fetchResponse = (responseType) => {
    return responses[responseType][Math.floor(Math.random() * responses[responseType].length)];
};

client.on(`message`, (msg) => {
    if(process.env.flag != flag)
        process.env.flag = flag;
    
    let user = msg.author;
    if(msg.channel.type != `dm` || user == client.user) return;
    let content = msg.content.toLowerCase();
    let response = ``;
    
    if(content.length > 250) {
        response = fetchResponse(`lazy`);
        console.log(`${user.tag}: ${msg.content}\nContent: ${content}\n> ${response}`);
        return user.send(response);
    }
    
    response = fetchResponse(`neutral`);
    let blacklist = [`eval`, `flag`, `msg`, `user`, `client`, `process`, `.`, `constructor`, `{`, `}`, `>`];
    
    for(let bannedToken of blacklist)
        if(content.includes(bannedToken))
            content = ``;
    
    try {
        content = eval(content);
    } catch(err) {
        content = ``;
    }
    
    if(content == flag) {
        response = fetchResponse(`amazed`);
        console.log(`${user.tag}: ${msg.content}\nContent: ${content}\n> ${response}`);
        return user.send(response);
    }
    
    console.log(`${user.tag}: ${msg.content}\nContent: ${content}\n> ${response}`);
    user.send(response);
});

client.login(`MTAzNTE4ODMxMDY3MjQxNjc4Mg.G8DSbU.a1dC_iJiVdYRtpOSZ8Dqi6w-WDkJH4Msxu_33g`);
