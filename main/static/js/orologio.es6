class Orologio{
    constructor(parent,co) {
        this.parent = parent;
        this.co = co;
        this.init();
    }

    init() {
        let me = this;
        me.hourOverride = 666;
        me.debug = true;
        me.quickDelay = 0.47 * 1000;
        me.slowDelay = 30 * 1000;
        me.version = "1.0.0";
        me.width = parseInt($(me.parent).css("width"), 10);
        me.height = parseInt($(me.parent).css("height"), 10);
        me.w = parseInt($(me.parent).css('width'));
        me.h = parseInt($(me.parent).css('height'));
        me.step = me.w / 32;
        me.fontsize = me.step / 4 ;
        me.light = [0.70,0.4,0,0,0,0,0,0.40,0.70,0.90,1,0.90];
        d3.select(me.parent).selectAll("svg").remove();
        me.svg = d3.select(me.parent).append("svg")
            .attr("viewBox", -me.w/2 +" "+ -me.h/2 +" "+ me.w + " " + me.h)
            .attr("width", me.w)
            .attr("height", me.h)
            ;
    }

    createPath(str,u){
        // Do not forget spaces between entities in str !!
        // Working example: str = "M 0,0 l 12,4 5,13 -5,0 -12,-17 z"
        // u is the scale unit. Try to link it to me.step
        let res = "";
        let items = str.split(" ")
        _.forEach(items, (item) => {
            if (item.includes(',')){
                let vals = item.split(',')
                res += (vals[0]*u)+","+(vals[1]*u)+" ";
            }else{
                res += item+" ";
            }
        });
        return res;
    }

    drawBack(){
        let me = this;
        me.circleback = me.svg.append('g')
            .attr("class","circlebacks")
            .append("g")
        ;
        me.circleback.append("circle")
            .attr("id","circleout")
            .attr("cx",me.step*7.2)
            .attr("cy",me.step*7.2)
            .attr("r",me.step)
            .style('stroke-width','1.5pt')
            .style('stroke','#101010')
            .style('fill','#B0A7A7')
        ;

        me.circleback.append("text")
            .attr("id","ZeHour")
            .attr("x",me.step*7.2)
            .attr("y",me.step*7.2)
            .attr("dy",(me.fontsize/2)+"pt")
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#303030')
            .style('font-family','Neucha' )
            .style('font-size',(me.fontsize*2)+'pt' )
            .style('text-anchor','middle' )
            .text("")
        ;


        me.circleback.append("circle")
             .attr("id","outercircle")
            .attr("cx",0)
            .attr("cy",0)
            .attr("r",me.step*8)
            .style('stroke','#101010')
            .style('stroke-width','1pt')
            .style('fill','#B0A7A7')
        ;
        me.circleback.append("circle")
            .attr("cx",0)
            .attr("cy",0)
            .attr("r",me.step*6)
            .style('stroke','#101010')
            .style('stroke-width','0.25pt')
            .style('fill','#D0C7C7')
        ;
        me.circleback.append("circle")
            .attr("cx",0)
            .attr("cy",0)
            .attr("r",me.step*5)
            .style('stroke','#606060')
            .style('stroke-width','1pt')
            .style('stroke-dasharray','1 1')
            .style('fill','transparent')
//            .style('opacity',0.50)
        ;
        me.circleback.append("circle")
            .attr("cx",0)
            .attr("cy",0)
            .attr("r",me.step*4)
            .style('stroke','#606060')
            .style('stroke-width','1pt')
            //.style('stroke-dasharray','5 2')
            .style('fill','transparent')
         //   .style("fill-opacity",0.1)
        ;
        me.circleback.append("circle")
            .attr("cx",0)
            .attr("cy",0)
            .attr("r",me.step*3)
            .style('stroke','#101010')
            .style('stroke-dasharray','5 5')
            .style('stroke-width','1pt')
            .style('fill','transparent')
        ;
        me.circleback.append("circle")
            .attr("cx",0)
            .attr("cy",0)
            .attr("r",me.step*2)
            .style('stroke','#101010')
            .style('stroke-dasharray','1 1')
            .style('stroke-width','1pt')
            .style('fill','transparent')
        ;
        me.circleback.append("circle")
            .attr("id","smallcentralcircle")
            .attr("cx",0)
            .attr("cy",0)
            .attr("r",me.step*0.125)
            .style('stroke','#101010')
            .style('stroke-width','1pt')
            .style('fill','transparent')
        ;
    }

    drawPerHour(){
        let me = this;
        me.ticks = me.svg.append('g')
            .selectAll('.ticks')
            .data([0,1,2,3,4,5,6,7,8,9,10,11])
            ;
        me.ticks_g = me.ticks.enter().append("g")
            .attr("class","ticks")
            .attr("transform",d=> 'rotate('+ (d-3)*30 +')')
            ;

        me.ticks_g.append("line")
            .attr("x1",me.step*5.70)
            .attr("y1",0)
            .attr("x2",me.step*6.5)
            .attr("y2",0)
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','transparent')
        ;

        me.ticks_g.append("line")
            .attr("x1",me.step*1.90)
            .attr("y1",0)
            .attr("x2",me.step*2.10)
            .attr("y2",0)
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','transparent')
        ;
        me.ticks_g.append("line")
            .attr("x1",me.step*4)
            .attr("y1",0)
            .attr("x2",me.step*4.30)
            .attr("y2",0)
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1.0pt')
            .style('fill','transparent')
        ;
        me.ticks_g.append("line")
            .attr("x1",me.step*2.25)
            .attr("y1",0)
            .attr("x2",me.step*2.75)
            .attr("y2",0)
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','3.0pt')
            .style('fill','transparent')
        ;

        me.ticks_g.append("a")
            .attr("xlink:href", function(d) {
                if (d == 11){
                    return "autochtons";
                }
            })
            .append("circle")
            .attr("class","imagecircle")
            .attr("id",d => "ic_"+d)
            .attr("cx",me.step*7.15)
            .attr("cy",0)
            .attr("r",2*me.step/3)
            .style('stroke','#273030')
            .style('stroke-linecap','round')
            .style('stroke-width','1.0pt')
            .style('fill','transparent')
            .style('cursor','pointer')
            //.style('opacity',0.25)
            .on('mouseover', (e, d) => {
                if (d == 11){
                    me.svg.select('#ic_'+d)
//                         .style('stroke','#A02020')
                        .style('stroke-width','5pt')
                    ;
                }
            })
            .on('mouseout',  (e, d) => {
                me.svg.selectAll('.imagecircle')
                    .style('stroke','#273030')
                    .style('stroke-width','1pt')
                    ;
            })


        ;
        me.ticks_g.append("circle")
            .attr("class","daylight")
            .attr("cx",me.step*3)
            .attr("cy",0)
            .attr("r",me.step/8)
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill', "#406080")
            .style('fill-opacity', d => me.light[d])
        ;
        me.ticks_g.append("circle")
            .attr("id",d => "polar_"+(d+1))
            .attr("cx",me.step*5)
            .attr("cy",0)
            .attr("r",4*me.step/6)
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','transparent')
            .style('fill-opacity', d => me.light[d])
        ;


        me.ticks_g.append("text")
            .attr("x",0)
            .attr("y",0)
            .attr("dy",(me.fontsize/2)+"pt")
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#303030')
            .style('font-family','Neucha' )
            .style('font-size',(me.fontsize)+'pt' )
            .style('text-anchor','middle' )
            .text(d => d+1)
            .attr("transform",d => {
                let adeg = (d-2)*30;
                let arad = (adeg/360)*2*Math.PI;
                let a = Math.cos(arad)*me.step*3.75;
                let b = Math.sin(arad)*me.step*3.75;
                let str = 'rotate('+ -(d-3)*30 +') translate('+a+','+b+')'
                return(str)
                }
            )
        ;
        me.ticks_g.append("image")
            .attr("id",d => "hd_"+d)
            .attr("xlink:href",d => "/static/main/svg/hd_"+(d+1)+".svg")
            .attr("width",me.fontsize*3)
            .attr("height",me.fontsize*3)
            .attr("x",-me.fontsize*1.5)
            .attr("y",-me.fontsize*1.5)
            .attr("transform",d => {
                let adeg = (d-2)*30;
                let arad = (adeg/360)*2*Math.PI;
                let a = Math.cos(arad)*(me.step*6.75+me.fontsize*1.5);
                let b = Math.sin(arad)*(me.step*6.75+me.fontsize*1.5);
                let str = 'rotate('+ -(d-3)*30 +') translate('+a+','+b+')'
                return(str)
            })
        ;

        // Hours
        me.ticks_g.append("rect")
            .attr("id",d => "rect_"+(d))
            .attr("class","linker")
            .attr("x",-7+me.step*6.0)
            .attr("y",-7)
            .attr("width",14)
            .attr("height",14)
            .style('fill','#7F8080')
            .style('stroke','#101010')
            .style('stroke-width','0.75pt')
            .style('cursor','pointer')
            .on('click', (e, d) => {
                console.log("Hour override ["+me.hourOverride+"]");
                if (me.hourOverride == (d+2)*2){
                    me.hourOverride = 666;
                }else{
                    me.hourOverride = (d+2)*2;
                }
                clearInterval(me.intervalSlow);
                me.intervalSlow = setInterval(function() {me.updateSlow();},me.quickDelay);
            })
        ;

        me.ticks.exit().remove();

    }

    drawPerRealHour(){
        let me = this;
        me.realhours = me.svg.append('g')
            .selectAll('.ticks')
            .data([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
            .enter()
            ;
        me.realhours_g = me.realhours.append("g")
            .attr("class","ticks")
            .attr("transform",d=> 'rotate('+ (d-11)*15 +')')
            ;

        me.realhours_g.append("line")
            .attr("x1",me.step*4.1)
            .attr("y1",0)
            .attr("x2",me.step*4.2)
            .attr("y2",0)
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','transparent')
        ;
        me.realhours_g.append("text")
            .attr("x",0)
            .attr("y",0)
            .attr("dy",(me.fontsize/4)+"pt")
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','0.5pt')
            .style('fill','#303030')
            .style('font-family','Neucha' )
            .style('font-size',(me.fontsize/2)+'pt' )
            .style('text-anchor','middle' )
            .text(d => d+"h00")
            .attr("transform",d => {
                let adeg = (d-11)*15;
                let arad = (adeg/360)*2*Math.PI;
                let a = Math.cos(arad)*me.step*3.3;
                let b = Math.sin(arad)*me.step*3.3;
                let str = 'rotate('+ -(d-11)*15 +') translate('+a+','+b+')'
                return(str)
                }
            )
        ;
    }

    drawArms(){
        let me = this;
        me.arms = me.svg.append('g');
        me.arms.append("path")
            .attr('id','minutes_arm')
            .attr("d",d => {
                let p = ""
                p += "M 0,-16 ";
                p += "m 5,0 l -5,-10 -5,10 5,-3 5,3 z";
                p += "M 0,-10 ";
                p += "l 1,-3 -1,-2 -1,2 1,3 z";
                let str = me.createPath(p,me.step / 20);
                return str;
                })
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#F08040')
            .style('opacity',0.9)
        ;

        me.arms.append("path")
            .attr('id','hours_main')
            .attr("d",d => {
                let str = me.createPath("M -4,-46 l 4,-9 4,9 -4,-2 -2 1 z",me.step / 10);
                return str;
                })
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#20A020')
            .style('fill-opacity',0.75)
            .on('mouseover',(e,x) => {
                console.log("z,p,zpzf")
            });
        ;

        me.arms.append("path")
            .attr('id','hours_fav1')
            .attr("d",d => {
                let str = me.createPath("M -4,-46 l 4,-9 4,9 -4,-2 -2 1 z",me.step / 10);
                return str;
                })
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#20A020')
            .style('fill-opacity',0.25)
        ;

        me.arms.append("path")
            .attr('id','hours_fav2')
            .attr("d",d => {
                let str = me.createPath("M -4,-46 l 4,-9 4,9 -4,-2 -2 1 z",me.step / 10);
                return str;
                })
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#20A020')
            .style('fill-opacity',0.25)
        ;


        me.arms.append("path")
            .attr('id','hours_def1')
            .attr("d",d => {
                let str = me.createPath("M -4,-46 l 4,-9 4,9 -4,-2 -2 1 z",me.step / 10);
                return str;
                })
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#A02020')
            .style('fill-opacity',0.25)
        ;

        me.arms.append("path")
            .attr('id','hours_def2')
            .attr("d",d => {
                let str = me.createPath("M -4,-46 l 4,-9 4,9 -4,-2 -2 1 z",me.step / 10);
                return str;
                })
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#A02020')
            .style('fill-opacity',0.25)
        ;

        me.arms.append("path")
            .attr('id','hours_opposition')
            .attr("d",d => {
                let str = me.createPath("M -4,-46 l 4,-9 4,9 -4,-2 -2 1 z",me.step / 10);
                return str;
                })
            .style('stroke','#202020')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#A02020')
            .style('fill-opacity',0.5)
        ;



        me.arms.append("path")
            .attr('id','seconds_arm')
            .attr("d",d => {
                let p = ""
                p += "M 0,-36 ";
                p += "m 5,0 l -5,-10 -5,10 5,-3 5,3 z";
                p += "M 0,-50 ";
                p += "l 1,-3 -1,-2 -1,2 1,3 z";
                let str = me.createPath(p,me.step / 20);
                return str;
                })
            .style('stroke','#101010')
            .style('stroke-linecap','round')
            .style('stroke-width','1pt')
            .style('fill','#F0C040')
            .style('opacity',0.9)
        ;

    }

    drawAll(){
        let me = this;
        me.drawBack();
        me.drawPerHour();
        me.drawPerRealHour();
        me.drawArms();
    }

    updateSlow(){
        let me = this;
        let d = new Date();
        let hours = d.getHours();
        if (me.hourOverride != 666){
            hours = me.hourOverride;
        }
        let hoursAngle = 360 * (Math.ceil(hours/2-2)/12)
        let hoursAngleO = 360 * (Math.ceil((hours+12)/2-2)/12)
        let hoursAngleF1 = 360 * (Math.ceil((hours+8)/2-2)/12)
        let hoursAngleF2 = 360 * (Math.ceil((hours-8)/2-2)/12)
        let hoursAngleD1 = 360 * (Math.ceil((hours+6)/2-2)/12)
        let hoursAngleD2 = 360 * (Math.ceil((hours-6)/2-2)/12)
        d3.select("#hours_main").attr('transform',"rotate("+hoursAngle+")")
        d3.select("#hours_fav1").attr('transform',"rotate("+hoursAngleF1+")")
        d3.select("#hours_fav2").attr('transform',"rotate("+hoursAngleF2+")")
        d3.select("#hours_opposition").attr('transform',"rotate("+hoursAngleO+")")
        d3.select("#hours_def1").attr('transform',"rotate("+hoursAngleD1+")")
        d3.select("#hours_def2").attr('transform',"rotate("+hoursAngleD2+")")

        clearInterval(me.intervalSlow);
        me.intervalSlow = setInterval(function() {me.updateSlow();},me.slowDelay);
    }

    updateQuick(){
        let me = this;
        let d = new Date();
        let minutes = d.getMinutes();
        let seconds = d.getSeconds();
        let minutesAngle = 360 * (minutes/60)
        let secondsAngle = 360 * (seconds/60)
        d3.select("#minutes_arm").attr('transform',"rotate("+minutesAngle+")")
        d3.select("#seconds_arm").attr('transform',"rotate("+secondsAngle+")")
        d3.select("#ZeHour").text(d => {
            if (me.hourOverride/2 - 2 != 331){
                return me.hourOverride/2 - 2;
            }else{
                return "-"
            }
        });
        if (me.hourOverride/2 - 2 == 331){
            d3.select("#hours_main").style('fill', '#202020');
            d3.select("#hours_opposition").style('fill', '#505050');
            d3.select("#hours_fav1").style('fill', '#303030');
            d3.select("#hours_fav2").style('fill', '#303030');
            d3.select("#hours_def1").style('fill', '#707070');
            d3.select("#hours_def2").style('fill', '#707070');
        }else{
            d3.select("#hours_main").style('fill', '#20A020');
            d3.select("#hours_opposition").style('fill', '#A05050');
            d3.select("#hours_fav1").style('fill', '#30A030');
            d3.select("#hours_fav2").style('fill', '#30A030');
            d3.select("#hours_def1").style('fill', '#A07070');
            d3.select("#hours_def2").style('fill', '#A07070');
        }
        clearInterval(me.intervalQuick);
        me.intervalQuick = setInterval(function() {me.updateQuick();},me.quickDelay);
    }

    perform(){
        let me = this;
        me.co.revealUniverse();
        me.drawAll();
        me.intervalQuick = setInterval(function() {me.updateQuick();},me.quickDelay);
        // The first refresh should pop sooner then me.slowDelay for updateSlow()
        me.intervalSlow = setInterval(function() {me.updateSlow();},me.quickDelay);
    }
}