import {incomeGrading,savingsGrading} from './levels.js'
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
  incomeGrading,
  savingsGrading,
  {
    type: 'graph',
      layout: 'force',
      symbolSize: 40,
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
  }
]