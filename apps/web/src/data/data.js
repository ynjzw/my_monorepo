export const titleList = [
  {
    text: "Title 1",
  },
  {
    text: "Title 2",
  },
  {
    text: "Title 3",
  }
]
export const optionList = [
   {
      type: 'graph',
      layout: 'force',
      symbolSize: 400,
      roam: true,
      data: [
        {
          name: 'Node 1',
          value: 10,
        },
        {
          name: 'Node 2',
          value: 10,
        },
        {
          name: 'Node 3',
          value: 10,
        }
      ],
      links: []
    },
    {
      type: 'graph',
      layout: 'force',
      symbolSize: 400,
      roam: true,
      data: [
        {
          name: 'Node 1',
          value: 10,
        },
        {
          name: 'Node 2',
          value: 10,
        },
        {
          name: 'Node 3',
          value: 10,
        }
      ],
      links: []
    },
    {
        type: 'tree',
        data: {
                    name: '我',
                    children: [
                    { name: '爸爸', value: 10 , children: [
                        { name: '爷爷', value: 10 },
                        { name: '奶奶', value: 10 }
                    ]},
                    { name: '妈妈', value: 10, children: [
                        { name: '外公', value: 10 },
                        { name: '外婆', value: 10 }
                    ]}
                    ]
                },
        top: '1%',
        left: '7%',
        bottom: '1%',
        right: '20%',
        symbolSize: 7,
        label: {
            position: 'left',
            verticalAlign: 'middle',
            align: 'right',
            fontSize: 9
        },
        leaves: {
            label: {
                position: 'right',
                verticalAlign: 'middle',
                align: 'left'
            }
        },
        emphasis: {
            focus: 'descendant'
        },
        expandAndCollapse: true,
        animationDuration: 550,
        animationDurationUpdate: 750
    }
]