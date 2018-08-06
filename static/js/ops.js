
function notify(type,icon,msg){

  $.notify({
      // options
      icon: icon,
      title: '<b>Ops+提示:</b>',
      message: msg,
    },{
      allow_dismiss: true,
      newest_on_top: false,
      type: type,
      delay: 5000,
      timer: 1000,
      icon_type: 'class',
      template: '<div data-notify="container" class="col-xs-11 col-sm-2 alert alert-{0}" role="alert">' +
        '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
        '<span data-notify="icon"></span> ' +
        '<span data-notify="title">{1}</span> ' +
        '<span data-notify="message">{2}</span>' +
        '<div class="progress" data-notify="progressbar">' +
          '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
        '</div>'+
      '</div>' 
    });

}

function custom_echart(k,v){
    // 基于准备好的dom，初始化echarts实例

    // 指定图表的配置项和数据
    var option = {
    tooltip : {
        trigger: 'axis',

    },
    legend: {
        data:['']
    },
    toolbox: {
        show : true,
        orient: 'vertical',
        x: 'right',
        y: 'center',
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    xAxis : [
        {
            type : 'category',
            data : []
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [],
    noDataLoadingOption: {
        text: '暂无数据',

    }
};
                   

    option.series = v.series;
    option.xAxis[0].data = v.xtime;
    option.legend.data = v.legend;
    var chart = echarts.init(document.getElementById(k), 'vintage');

        // 使用刚指定的配置项和数据显示图表。
    chart.setOption(option);

  }      


function monitor_echart(k,v,xtime,name,legend,units){
    var option = {
    grid: {
      x2:40,
      y2:90,
    },
    title: {
        text: '',
        x:'left',
        y:'top',
        textAlign:'left'
    },
    tooltip : {
        trigger: 'axis',
    },
    legend: {
        y: 'bottom',
        data:[]
    },
    toolbox: {
        show : true,
        orient: 'vertical',
        x: 'right',
        y: 'center',
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    xAxis : [
        {
            type : 'category',
            data : [],
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value}'
            },
        },

    ],
    series : []
};

               
    option.title.text = name;
    option.yAxis[0].axisLabel.formatter = '{value} ' + units;
    option.series = v;
    option.xAxis[0].data = xtime;
    option.legend.data = legend;
    var chart = echarts.init(document.getElementById(k), 'vintage');

        // 使用刚指定的配置项和数据显示图表。
    chart.setOption(option);

  }                  
