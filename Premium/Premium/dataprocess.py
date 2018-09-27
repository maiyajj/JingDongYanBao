# coding=utf-8
# @File  : dataprocess.py
# @Author: 'maiyajj'
# @Date  : 2018/9/26

from .sql import Sql
import itertools
import xlwt


class DataProcess(object):
    sql = Sql()
    db = ''

    def search(self):
        categories = self.sql.get_all_category(self.db)
        response = {}
        for i in categories:
            response[i] = self.sql.get_all_data_form_category(self.db, category=i)

        premium_prices = {}
        for category, resp in response.items():
            premium_price = {}
            premium_prices[category] = premium_price
            for i in resp:
                prices, premiums = float(i[5]), eval(i[6])
                for premium in premiums:
                    name, price = premium
                    if name not in premium_price:
                        premium_price[name] = {}
                    if price not in premium_price[name]:
                        premium_price[name][price] = set()
                    premium_price[name][price].add(prices)
            for name, premiums in premium_price.items():
                for premium, prices in premiums.items():
                    try:
                        max_price = max(prices)
                        min_price = min(prices)
                    except:
                        max_price = min_price = prices
                    premium_price[name][premium] = [min_price, max_price]
                #list(combinations([1, 2, 3], 2))
        # tmp = []
        # for name, premiums in premium_price.items():
        #     tmp.append([name + ':' + i for  i in premiums.keys()])
        print(premium_prices)
        self.premium_prices = premium_prices
        # self.write_xls()


        # generates = list(itertools.product(*tmp))
        # for i in generates:
        #     name, price = i[0].split(':')
        #     result = premium_price[name][price]
        #     for ii in i:
        #         name, price = ii.split(':')
        #         result = result & premium_price[name][price]
        #         if result:
        #             print(result)

    def write_xls(self):
        # 单元格格式
        easyxf1 = xlwt.easyxf(u'font: height 320, name 宋体, colour_index 70, bold on;'
                              u'align: wrap on, vert top, horiz centre;'
                              u'borders: top thin, left thin, right thin;')

        easyxf2 = xlwt.easyxf(u'font: height 220, name 宋体;'
                              u'align: wrap on, horiz left;'
                              u'borders: right thin;')
        premium_prices = self.premium_prices
        file_name = '奥克斯'
        category = '空调'


        # 检查设备报告路径是否存在
        def check_path():
            nonlocal file_name
            parent_path = r'./report'
            xls_file = r'%s/%s.xls' % (parent_path, file_name)  # 文件路径及名称
            return xls_file

        # 启动脚本首先运行此函数，会生成报告模板待填充数据
        def run():
            xls_file = check_path()
            book = xlwt.Workbook(encoding='utf-8')
            sheet = book.add_sheet('数据', cell_overwrite_ok=True)
            write_data(sheet)
            book.save(xls_file)

        # 报告模板设计，根据手动设计报告模板，使用函数实现
        def write_data(sheet):
            nonlocal premium_prices, file_name, category

            for i in range(26):
                sheet.col(i).width = 256 * 13  # 设置单元格宽度
            sheet.col(26).width = 256 * 16

            col = 2
            col1 = col + 4
            col2 = col1 + 3
            col3 = col2 + 4
            col4 = col3 + 5
            col5 = col4 + 4

            row = 0
            sheet.write_merge(row, row, col, col1 - 1, '全面保障 保费', easyxf1)
            sheet.write_merge(row, row, col1, col2 - 1, '延长保修 保费', easyxf1)
            sheet.write_merge(row, row, col2, col3 - 1, '意外保护 保费', easyxf1)
            sheet.write_merge(row, row, col3, col4 - 1, '京东服务+ 保费', easyxf1)
            sheet.write_merge(row, row, col4, col5 - 1, '特色服务 保费', easyxf1)
            sheet.write_merge(row, row + 1, col5, col5, '其他 保费', easyxf1)

            row += 1
            sheet.write(row, 0, '品牌', easyxf2)
            sheet.write(row, 1, '类目', easyxf2)
            sheet.write(row, col, '价格区间', easyxf2)
            sheet.write(row, col + 1, '全保修7年', easyxf2)
            sheet.write(row, col + 2, '全保修8年', easyxf2)
            sheet.write(row, col + 3, '全保+清洗', easyxf2)
            sheet.write(row, col1 + 1, '价格区间', easyxf2)
            sheet.write(row, col1 + 2, '延保至8年', easyxf2)
            sheet.write(row, col1 + 3, '延保至9年', easyxf2)
            sheet.write(row, col2 + 1, '价格区间', easyxf2)
            sheet.write(row, col2 + 2, '意外保2年', easyxf2)
            sheet.write(row, col2 + 3, '意外保3年', easyxf2)
            sheet.write(row, col3 + 1, '价格区间', easyxf2)
            sheet.write(row, col3 + 2, '意外保2年', easyxf2)
            sheet.write(row, col3 + 3, '意外保3年', easyxf2)
            sheet.write(row, col4 + 1, '价格区间', easyxf2)
            sheet.write(row, col4 + 2, '空调清洗', easyxf2)
            sheet.write(row, col4 + 3, '油洗套装', easyxf2)
            sheet.write(row, col4 + 4, '油洗冰套装', easyxf2)

            '''
                        品牌	类目	价格区间	全保修3年	全保修5年	其他	价格区间	延长保2年	延长保3年	换新保2年	换新保3年	其他	价格区间	意外保2年	意外保3年	其他	价格区间	4年整机保修	6年整机保修	滚筒清洗	波轮清洗	价格区间	冰洗套装	油洗套装	油洗冰套装
                        '''
            rows = max([len(i) for i in premium_prices.values()])
            row += 1
            sheet.write_merge(row, row + rows, 0, 0, '品牌', easyxf2)
            sheet.write_merge(row, row + rows, 1, 1, '类目', easyxf2)


            row += 1
            sheet.write(row, 0, '价格区间', easyxf2)
            sheet.write(row, 0, '全保修3年', easyxf2)
            sheet.write(row, 0, '全保修5年：', easyxf2)
            sheet.write(row, 0, '手机型号：', easyxf2)
            row += 1

            sheet.write(row, 0, 'APP及版本号：', easyxf2)
            sheet.write_merge(row, row, 1, 8, app_name + app_ver, easyxf2)
            # row += 1
            #
            # start_time = time.strftime('%Y-%m-%d %X')
            # sheet.write(row, 0, '开始时间：', easyxf2)
            # sheet.write_merge(row, row, 1, 8, start_time, easyxf2)
            # row += 1
            #
            # sheet.write(row, 0, '结束时间：', easyxf2)
            # sheet.write_merge(row, row, 1, 8, start_time, easyxf2)
            # row += 1
            #
            # sheet.write(row, 0, '持续时间：', easyxf2)
            # sheet.write_merge(row, row, 1, 8, '0:00:00', easyxf2)
            # row += 1
            #
            # sheet.write(row, 0, '执行用例数：', easyxf2)
            # sheet.write_merge(row, row, 1, 8, 0, easyxf2)
            # row += 1
            #
            # sheet.write(row, 0, '执行结果：', easyxf2)
            # sheet.write_merge(row, row, 1, 8, '通过 0； 失败 0； 执行错误 0； 人工检查 0；', easyxf2)
            # row += 1
            #
            # sheet.write_merge(row, row, 0, 8, '', easyxf7)
            # row += 1
            # sheet.write_merge(row, row, 0, 8, '用例执行情况：', easyxf7)
            # row += 1
            # sheet.write_merge(row, row, 0, 8, '', easyxf7)
            # row += 1
            #
            # write_list = ['禅道ID', '用例名称', '是否执行', '执行次数', '通过', '失败', '未知错误', '人工检查', '最终结果']
            # for i in write_list:
            #     sheet.write(row, write_list.index(i), i, easyxf5)
            # row += 1

        run()
