import {incomeGrading,savingsGrading} from './levels.js'
import {stageOne1} from './lifeStage.js'
export const titleList = [
  {
    text: "before 18",
  },
  {
    text: "18 to 60",
  },
  {
    text: "after 60",
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