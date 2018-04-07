var express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
var FinanceData = require('../models/finance.js');

/* GET users listing. */
router.get('/:inputdate?', function(req, res, next) {

    var indate = req.params.inputdate;
    // console.log("Retrieve data for " + indate);
    FinanceData.find({date:  {$lte: indate}}).sort({date:-1}).limit(3).exec(function(err, findata) {
        if (err) throw err;
        // console.log(findata);
        res.json(findata);
    });

});

module.exports = router;
