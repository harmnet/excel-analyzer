<template>
    <div>
      <h1>销售数据表格</h1>
      <table :style="tableStyle">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col" :style="thStyle">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in tableData" :key="index">
            <td v-for="col in columns" :key="col" :style="tdStyle">{{ row[col] }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="exportToWord">导出Word</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        columns: ['序号', '商品名称', '销售额', '销量', '单价'],
        tableData: [],
        tableStyle: {
          width: '100%',
          borderCollapse: 'collapse',
          margin: '20px 0',
          fontFamily: 'Arial, sans-serif'
        },
        thStyle: {
          backgroundColor: '#f2f2f2',
          border: '1px solid #ddd',
          padding: '12px',
          textAlign: 'left'
        },
        tdStyle: {
          border: '1px solid #ddd',
          padding: '12px',
          textAlign: 'left'
        }
      }
    },
    created() {
      // 生成示例数据
      this.tableData = Array.from({length: 10}, (_, i) => ({
        序号: i + 1,
        商品名称: `商品${i + 1}`,
        销售额: Math.floor(Math.random() * 4000) + 1000,
        销量: Math.floor(Math.random() * 400) + 100,
        单价: Math.floor(Math.random() * 90) + 10
      }))
    },
    methods: {
      exportToWord() {
        // 创建HTML内容
        const html = `
          <html>
            <body>
              <table border="1">
                <tr>${this.columns.map(col => `<th>${col}</th>`).join('')}</tr>
                ${this.tableData.map(row => `
                  <tr>${this.columns.map(col => `<td>${row[col]}</td>`).join('')}</tr>
                `).join('')}
              </table>
            </body>
          </html>
        `
        
        // 创建Blob对象
        const blob = new Blob([html], {type: 'application/msword'})
        
        // 创建下载链接
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = 'sales_data.doc'
        
        // 触发下载
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      }
    }
  }
  </script>
  