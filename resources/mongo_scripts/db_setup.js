db.positive_frequencies.drop()
db.negative_frequencies.drop()
db.dictionary.drop()

var mapfunction = function(){
    var words = this.text.split(' ');
    for(word in words){
        emit(words[word],1); 
    }
}

var reducefunction = function (word, polarities){
    return Array.sum(polarities)
}



db.runCommand(
    {
        mapReduce: "training",
        map: mapfunction,
        reduce: reducefunction,
        query: {"polarity":"pos"},
        out: "positive_frequencies"
    }
)


db.runCommand(
    {
        mapReduce: "training",
        map: mapfunction,
        reduce: reducefunction,
        query: {"polarity":"neg"},
        out: "negative_frequencies"
    }
)




var neg_map = function(){
    emit(this._id, {"neg_freq": this.value});
}

var pos_map = function(){
    emit(this._id, {"pos_freq": this.value})
}

var r = function(key, values){
    var result = {
        "neg_freq": null,
        "pos_freq": null
    };

    values.forEach(function(value){
        if(value.neg_freq !==null){
            result.neg_freq = value.neg_freq;
        }
        if(value.pos_freq !==null){
            result.pos_freq = value.pos_freq;
        }
    });

    return result;

}

db.negative_frequencies.mapReduce(neg_map, r, {out: {reduce: 'dictionary'}});

db.positive_frequencies.mapReduce(pos_map, r, {out: {reduce: 'dictionary'}});




db.dictionary.update({"value.neg_freq":{$exists:false}}, {$set: {"value.neg_freq": 0}}, false, true)
db.dictionary.update({"value.pos_freq":{$exists:false}}, {$set: {"value.pos_freq": 0}}, false, true)

db.dictionary.update({"value.neg_freq":null}, {$set: {"value.neg_freq": 0}}, false, true)
db.dictionary.update({"value.pos_freq":null}, {$set: {"value.pos_freq": 0}}, false, true)

