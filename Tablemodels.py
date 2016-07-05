

def curspatial(self):
    from pysqlite2 import dbapi2 as sql
    self.sql_connection = sql.Connection(self.mainDB)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
    self.cursorspatial = sql.Cursor(self.sql_connection)
    self.sql_connection.enable_load_extension(1)
    self.sql_connection.load_extension('libspatialite-2.dll') 
    


class TableModel(object):

    def __init__(self, name, db, cursor, connection):
        'Table model to input and output database tables'
        self.name = name
        self.database = db
        self.connect = connection
        self.cursor = cursor
        self.valueDic = {}
        self.rows = []
        self.fields = []        
        self.fieldTypeDic = {}
        self.fieldTypes = {'DOUBLE': 'D',
                           'FLOAT':'F',
                           'INTEGER': 'N',
                           'BOOL': 'C',
                           'REAL': 'F',
                           'TEXT':'C',
                           'POLYGON':5,
                          'POINT':1,
                          'LINESTRING':3,
        
        
                           }        
                
    def sqlCommands(self):
        'sql for retrieval and insertion'
        self.sqlFieldInfo = 'PRAGMA table_info({0})'
        self.sqlSelect = 'SELECT {0} FROM {1} ' 
        self.sqlInsert = 'INSERT INTO {0}({1}) VALUES ({2})'
        self.sqlCreate = "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = '{0}'"
        self.sqlUpdate = "UPDATE {0} "
        self.sqlSet = "SET {0} = ? "
        self.sqlSelectByID = 'PK_UID BETWEEN ? AND ?' 
        self.sqlWhere = 'WHERE {0}'
        
    def fieldsGen(self):
        'get table fields and create name:type dictionary'
        fields = self.sqlFieldInfo, self.name
        self.curX(fields)
        retFields = self.curAll()

        for field in retFields:
            fieldval = field[1]
            typeval = field[2]
            self.fieldTypeDic[fieldval] = typeval
            self.fields.append(fieldval)
            
        
    def getFieldsByType(self, type):
        'get name fo fields for a given field type'
        typeResults = find_key(self.fieldDic, type)
        return typeResults
    
    def find_key(self,dic, val):
        """return the key of dictionary dic given the value"""
        return [k for k, v in dic.iteritems() if v == val][0]

    def changeFieldOrder(self):
        'adjust recorded order of fields'
        return

    def valuesGen(self,params,min=0,max=None):
        'get selected rows of data'
        self.rows=[]
        if max == None:
            params = (fields, self.name)
            select = self.sqlSelect, params
        else:
            params = (fields, self.name)
            args= min, max
            select = self.sqlSelect+ self.sqlSelectByID, params, args 
        self.curX(select)
        valResults = self.curAll()

        for COUNTER, field in enumerate(self.fieldDic):
            self.valueDic[field] = []
            for COUNTY,value in enumerate(valResults):
                dic = {}
                dic[COUNTY] = value[COUNTER]
                self.valueDic[field].append(dic)
                self.rows.append(value))
        
    def tableDicGen(self):
        'create tkintertable representation of selected data '

                
        dataDic = {}
        valueRange = len(self.rows)
        for i in range(1,valueRange+1):
            dataDic[str(i)] = {}
            
        for COUNTROW, row in enumerate(self.rows):
            for COUNTERX, field in enumerate(self.fields):
                for  value in row:

                    dataDic[COUNTROW][field] = value 
      
        self.tableDic = dataDic    
    
    def csvRowsGen(self,sep=','):
        'create CSV representation of selected data'
        for COUNTER, column in enumerate(self.fields):

            header = ''
            if COUNTER != len(self.field)-1:
                header += column + sep
            else:
                header += column +'\n'
                
        self.csvFields = header
        self.csvRows = []
        for row in self.rows:
            line = ''
            for val in row:
                if COUNTER != len(row)-1:
                    line += val + sep
                else:
                    line += val + '\n'
             self.csvRows.append(line)                   
    
    def xlsDicGen(self):
        'create xls representation of selected data'
        self.xlsFields - self.fields
        self.xlsRows = self.rows
        


    def insert(self, params, args):  
        'insert into table'  
        insertsql = self.sqlInsert, params, args
        self.curX(insertsql)
        self.connect.commit()
    
    def constraintGen(self,params):
        where = self.sqlWhere.format(params)
    
    def update(self, params, args, where=None):

        newparams = ''
        for param in params:
            if count == len(params)-1:
                
                newparams = self.sqlSet.format(param) + ','
            else:
                newparams = self.sqlSet.format(param)
        
        if where:
            updatesql =  self.sqlUpdate.format(self.name) + self.constraintGen(where), args
        else
            updatesql = self.sqlUpdate.format(self.name) + newparams,args 
        self.curX(updatesql)
        self.connect.commit()  
         
    def curX(self,sql,args=()):
        'execute sql statements'
        statement = sql[0]
        params = sql[1]
        self.cursor.execute(statement.format(*params), *args)        
        return

    def curIn(self,sql):
        'execute sql statements'
        self.curX(sql)
        self.connect.commit()        
        return
    
    def curAll(self,):
        results = self.cursor.fetchall()  
        return  results
    
    def curOne(self,):
        self.cursor.fetchone()  
        return  
                
        
class GeoTableModel(TableModel):
    
        
    def geoSQL(self):
        self.sqlTransform = 'Transform(Geometry,{0}')
        self.sqlGeomFromText = 'ST_GeomFromText({0})'
        self.sqlPointFromText = 'PointFromText({0},{1})'
        self.sqlLineFromText = 'LineFromText({0},{0})'
        self.sqlNumInteriorRings = 'NumInteriorRing({0})'
        self.sqlGeometryRow = 'GeometryN({0})'
        self.sqlGeomAsText = 'ST_GeomAsText({0})'
        self.sqlEnvelope = 'Envelope(Geometry)'
        self.sqlSrid = 'SRID(Geometry)'
        self.sqlArea = 'ST_Area(Geometry)'
        self.sqlIntersect = 'Intersects(Geometry,{0})  '
        self.sqlWithin = 'Within(Geometry,{0}) '
        self.sqlContains = 'Contains(Geometry,{0}) '
        self.sqlIntersection = 'Intersection(Geometry,{0}) '
        self.sqlCrosses = 'Crosses(Geometry,{0})'
        self.sqlBuildMBR = 'BuildMBR({0}) '
        self.sqlMBRMaxX = 'MBRMaxX(Geometry) '
        self.sqlMBRMaxY = 'MBRMaxY(Geometry) '
        self.sqlMBRMinX = 'MBRMinX(Geometry) '
        self.sqlMBRMinY = 'MBRMinY(Geometry) '
        self.sqlCentroid = 'Centroid(Geometry)'
        self.sqlGeomType = 'GeometryType(Geometry'
        self.sqlX = 'X(Geometry)'
        self.sqlY = 'Y(Geometry)'
        self.sqlBuffer = 'Buffer(Geometry, {0})
        self.sqlMBRContains = 'MbrContains(Geomtry,{0})'
        self.sqlMBRWithin = 'MbrWithin(Geomtry,{0})'
        self.sqlMBRIntersects = 'MbrIntersects(Geomtry,{0})'
        self.sqlMBROverlaps = 'MbrOverlaps(Geomtry,{0})'
        
    def getGeoType(self):
        type = self.sqlSelect, (self.sqlGeomType, self.name)
        self.curX(type)
        self.type = self.curOne()[0]
        
    def geometryAsText(self):
        
    def getGeoms(self,rows):
    
    def getMBR(self,rows):

    def srid(self):
                
    def sridScrape(self, tablename):
        sql = "SELECT SRID FROM geom_cols_ref_sys WHERE f_table_name = '%s'" % tablename
        self.cursorspatial.execute(sql)
        srid = self.cursorspatial.fetchone()[0]
        return srid
        
    def parseGeo(self, geometry):
        if geometry.find('POINT')!= -1:
            geom = geometry.split('(')[1].replace(')','')
            geomlist = map(float,geom.split())
        else:

            partsList = []
            geom = geometry.split('((')[1].replace('))','')
            partSplit = geom.split('), (')
            for part in partSplit:
                geomlist = []
                geomsplit = part.split(', ')
                for COUNTER,geoms in enumerate(geomsplit):
                       
                        xy = map(float,geoms.split())
                        
                        geomlist.append(xy)
                partsList.append(geomlist)
                
        return partsList

    def reverseParseGeo(self, shpReader):
        geomtype = find_key(self.fieldTypes, shpReader.shapeType )
        if geomtype == 'POINT':
            WKTlist = []
            WKTtemplate = 'POINT(%f %f)'
            shapes = shpReader.shapes()
            for shape in shapes:
                pnt = shape.points[0]
                WKT = WKTtemplate % (pnt[0], pnt[1])
                WKTlist.append(WKT)
        elif geomtype == 'POLYGON':
            WKTtemplate = 'POLYGON(('
            WKTlist = []
            shapes = shpReader.shapes()
            for shape in shapes:
                WKT = WKTtemplate
                points =shape.points
                firstCoords = points[0] 
                countVal = 0
                for COUNTER,coords in enumerate(points):
                    if COUNTER != len(shape.points)-1:
                        if coords == firstCoords and COUNTER != countVal:
                            WKT += str(coords[0]) + ' '+ str(coords[1])+ '), ('
                            firstCoords = points[COUNTER+1]
                            countVal = COUNTER +1                            
                        else:
                            WKT += str(coords[0]) + ' '+ str(coords[1])+ ', '

                    else:
                        WKT += str(coords[0]) + ' '+ str(coords[1])+ '))'
                WKTlist.append(WKT)
        elif geomtype == 'LINESTRING':
            WKTtemplate = 'LINESTRING('
            WKTlist = []
            shapes = shpReader.shapes()
            for shape in shapes:
                WKT = WKTtemplate
                for COUNTER,coords in enumerate(shape.points):
                    if COUNTER != len(shape.points)-1:
                        WKT += str(coords[0]) + ' '+ str(coords[1])+ ', '
                    else:
                        WKT += str(coords[0]) + ' '+ str(coords[1])+ ')'
                WKTlist.append(WKT)                   
        return WKTlist
    def unit(self):
        
    def shapeRowsGen(self):

        
    def exportRows(self,row):
        
    def getCreateStatment(self):
        create = self.sqlCreate, self.name
        
    def multiplier(self):
        
        
    def 