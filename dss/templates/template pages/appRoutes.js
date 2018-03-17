/*var mongoose = require('mongoose');
mongoose.connect('mongodb://adminuser:Jam%4007&22&09@ds063630.mlab.com:63630/csgojam');

var express = require('express'),
    steam   = require('steam-login');
var dbcollections = require('./dbschema');

app.use(require('express-session')({ resave: false, saveUninitialized: false, secret: 'a secret' }));
app.use(steam.middleware({
    realm: 'http://localhost:3000/',
    verify: 'http://localhost:3000/verify',
    apiKey: '743577A2D5AD0CE07E731BF26433F2F3'}
));*/
var express = require('express');
var app = express();

app.set('views', __dirname);
app.set('view engine', 'ejs');
var loggedInUser = null;

app.get('/', function(req, res) {
	res.render('login',{
    	"user" : loggedInUser,
    });
	
    //console.log(dbcollections.usersSchema);
    //res.send(req.user).end();
});

app.get('/b',function(req, res){
	res.render('b');
});

/*app.get('/authenticate', steam.authenticate(), function(req, res) {
    console.log("Authentcate");
    res.redirect('/');

    //res.send(req.user).end();
});
*/
/*app.get('/verify', steam.verify(), function(req, res) {
    
    
	var users = dbcollections.usersModel;
	//console.log(req.user.steamid);
	users.find({steamAttr:req.user.steamid},function(err,data){
		console.log(req.user);
		loggedInUser = req.user;
		console.log("Logedin user");
		console.log(loggedInUser);
		if(data.length===0) 
		{
			console.log("nulllllll");
			var u = new dbcollections.usersModel({
			"steamAttr": ""+req.user.steamid,
			"steamName" : ""+req.user.username,
		    "points": "100",
		    "referrer": "String",
		    "type": "String",
		    "is_active": 1,
		    "totalWithdrawal": "String",
		    "totalDeposit": "String",
		    "totalWon": "String",
		    "totalLost": "String",
		    lastLogin : new Date(),
		    imageURL : ""+req.user.avatar.large	});

		    u.save();
		    res.redirect('/');
		}
		else{
			if(req.user.username!=data[0].steamName)
			{	
				users.updateOne(data[0],{$set:{steamName:""+req.user.username}},function(nameErr,nameData){
					if(!!nameErr) console.log("Error updating Name");
					else
						console.log("name updated");	
				});
			}
			if(req.user.avatar.large != data[0].imageURL)
			{
				users.updateOne(data[0],{$set:{imageURL:""+req.user.avatar.large}},function(nameErr,nameData){
					if(!!nameErr) console.log("Error updating Image");
					else
						console.log("image updated");	
				});
			}
			res.redirect('/');
		}
	});
	console.log("verify");
});

app.get('/logout', steam.enforceLogin('/'), function(req, res) {
    req.logout();
    res.redirect('/');
});
*/
app.listen(3000);
console.log('listening');