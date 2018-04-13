const mongoose   = require('mongoose')

const FinanceSchema = new mongoose.Schema({
	date: {
		type: String,
		required: true
	},
	close: [{
        stock: {
            type: String,
    		trim: true,
    		required: true
        },
        value: {
            type: Number,
    		trim: true,
    		required: true
        }
	}],
    parameters: {
		"nifty_log_return_1" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"nifty_log_return_2" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"nifty_log_return_3" : {
            type: Number,
    		trim: true,
    		required: true
        },
        "aord_log_return_2" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"dax_log_return_0" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"nyse_log_return_2" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"dax_log_return_2" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"hangseng_log_return_2" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"aord_log_return_1" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"dax_log_return_1" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"nikkei_log_return_1" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"snp_log_return_3" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"snp_log_return_1" :{
            type: Number,
    		trim: true,
    		required: true
        },
		"nyse_log_return_1" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"nikkei_log_return_2" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"djia_log_return_2" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"snp_log_return_2" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"aord_log_return_0" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"nikkei_log_return_0" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"nifty_log_return_positive" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"nifty_log_return_negative" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"djia_log_return_1" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"hangseng_log_return_1" :{
            type: Number,
    		trim: true,
    		required: true
        },
		"nyse_log_return_3" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"hangseng_log_return_0" : {
            type: Number,
    		trim: true,
    		required: true
        },
		"djia_log_return_3" : {
            type: Number,
    		trim: true,
    		required: true
        }
    }
}, { collection: 'finance' })

FinanceData = mongoose.model('FinanceData', FinanceSchema)

module.exports = FinanceData
