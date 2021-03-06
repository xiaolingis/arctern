# Copyright (C) 2019-2020 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyspark.sql import SparkSession
from arctern_pyspark import register_funcs
from pyspark.sql.types import *
from pyspark.sql.functions import col

import random
import shutil
import os
import json
import sys

base_dir = './data/'

def clear_result_dir(dir_name):
    try:
        shutil.rmtree(dir_name)
    except IOError:
        # print('IO error happened while deal with dir: %s' % dir_name)   
        pass
        

def get_data(base_dir, fname):
    return os.path.join(base_dir, fname)

def read_data(spark, base_dir, data):
    ext = os.path.splitext(data)[1][1:]
    if ext == 'json':
        return spark.read.json(get_data(base_dir, data)).cache()
    elif ext == 'csv':
        # return spark.read.csv(get_data(base_dir, data)).cache()
        return spark.read.format('csv').options(header='true', sep='|').load(get_data(base_dir, data)).cache()

def to_txt(file_dir, df):
    df.write.text(file_dir)

def save_result(file_dir, df):
    tmp = '/tmp'
    df.write.csv(os.path.join(tmp, file_dir))
    # df.write.json(os.path.join(tmp, file_dir))

def get_test_config(config_file):
    with open(config_file, 'r') as f:
        configs = json.load(f)
    return configs

# ------------------------------------ test part ------------------------------------
def run_test_st_point(spark):
    # ***********************************************
    # generate st_point from json data loaded
    # ***********************************************

    data = "points.csv"
    table_name = 'test_points'
    sql = "select st_point(x_float, y_float) from test_points"
    
    df = read_data(spark, base_dir, data)
    df = df.withColumn("x_float", col("left").cast("double")).withColumn("y_float", col("right").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_envelope_aggr_1(spark):
    
    data = "envelope_aggr.csv"
    table_name = 'test_envelope_aggr_1'
    sql = "select st_envelope_aggr(geos) as my_envelope from test_envelope_aggr_1"
    
    df = read_data(spark, base_dir, data)
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_envelope_aggr_curve(spark):
    
    data = "envelope_aggr_curve.csv"
    table_name = 'test_envelope_aggr_curve'
    sql = "select st_envelope_aggr(geos) as my_envelope from test_envelope_aggr_curve"
    
    df = read_data(spark, base_dir, data)
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_envelope_aggr_2(spark):
    
    data = "points.csv"
    table_name = 'envelope_aggr_2'
    sql = "select st_envelope_aggr(arealandmark) from (select st_point(x_float, y_float) as arealandmark from envelope_aggr_2)"
    
    df = read_data(spark, base_dir, data)
    df = df.withColumn("x_float", col("left").cast("double")).withColumn("y_float", col("right").cast("double"))
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)
    
def run_test_st_isvalid_1(spark):
    
    data = "isvalid.csv"
    table_name = 'test_isvalid'
    sql = "select st_isvalid(geos) as is_valid from test_isvalid"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_isvalid_curve(spark):
    
    data = "isvalid_curve.csv"
    table_name = 'test_isvalid_curve'
    sql = "select st_isvalid(geos) as is_valid from test_isvalid_curve"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_union_aggr_2(spark):
    data = 'union_aggr.csv'
    table_name = 'test_union_aggr_2'
    sql = "select st_union_aggr(geos) as union_aggr from test_union_aggr_2"

    df = read_data(spark, base_dir, data)
    df.show()
    df.printSchema()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_union_aggr_curve(spark):
    data = 'union_aggr_curve.csv'
    table_name = 'test_union_aggr_curve'
    sql = "select st_union_aggr(geos) as union_aggr from test_union_aggr_curve"

    df = read_data(spark, base_dir, data)
    df.show()
    df.printSchema()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_intersection(spark):

    data = "intersection.csv"
    table_name = 'test_intersection'
    sql = "select st_intersection(left, right) from test_intersection"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_intersection_curve(spark):

    data = "intersection_curve.csv"
    table_name = 'test_intersection_curve'
    sql = "select st_curvetoline(st_intersection(left, right)) from test_intersection_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_convexhull(spark):
    data = "convexhull.csv"
    table_name = 'test_convexhull'
    sql = "select st_convexhull(geos) as geos from test_convexhull"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_convexhull_curve(spark):
    # this test is to test convexhull's result is curve, which not support in postgis, we need to convert arctern result to basic types, then compare
    data = "convexhull_curve.csv"
    table_name = 'test_convexhull_curve'
    sql = "select st_curvetoline(st_convexhull(geos)) as geos from test_convexhull_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer(spark):
    data = "buffer.csv"
    table_name = 'test_buffer'
    sql = "select st_buffer(geos, 0) as geos from test_buffer"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer1(spark):
    data = "buffer.csv"
    table_name = 'test_buffer1'
    sql = "select st_buffer(geos, 1) as geos from test_buffer1"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer2(spark):
    data = "buffer.csv"
    table_name = 'test_buffer2'
    sql = "select st_buffer(geos, 5.5) as geos from test_buffer2"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer3(spark):
    data = "buffer.csv"
    table_name = 'test_buffer3'
    sql = "select st_buffer(geos, 100) as geos from test_buffer3"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer4(spark):
    data = "buffer.csv"
    table_name = 'test_buffer4'
    sql = "select st_buffer(geos, -0.33) as geos from test_buffer4"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer5(spark):
    data = "buffer.csv"
    table_name = 'test_buffer5'
    sql = "select st_buffer(geos, -2) as geos from test_buffer5"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer6(spark):
    data = "buffer.csv"
    table_name = 'test_buffer6'
    sql = "select st_buffer(geos, -80) as geos from test_buffer6"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer_curve(spark):
    data = "buffer_curve.csv"
    table_name = 'test_buffer_curve'
    sql = "select st_curvetoline(st_buffer(geos, 0)) as geos from test_buffer_curve"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_buffer_curve1(spark):
    data = "buffer_curve.csv"
    table_name = 'test_buffer_curve1'
    sql = "select st_curvetoline(st_buffer(geos, 1)) as geos from test_buffer_curve1"
    
    df = read_data(spark, base_dir, data)
    # df = df.withColumn("d", col("distance").cast("double"))
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_envelope(spark):
    data = "envelope.csv"
    table_name = 'test_envelope'
    sql = "select st_envelope(geos) as geos from test_envelope"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_envelope_curve(spark):
    data = "envelope_curve.csv"
    table_name = 'test_envelope_curve'
    sql = "select st_envelope(geos) as geos from test_envelope_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_centroid(spark):
    data = "centroid.csv"
    table_name = 'test_centroid'
    sql = "select st_centroid(geos) as my_centroid from test_centroid"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_centroid_curve(spark):
    data = "centroid_curve.csv"
    table_name = 'test_centroid_curve'
    sql = "select st_centroid(geos) as my_centroid from test_centroid_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_length(spark):
    data = "length.csv"
    table_name = 'test_length'
    sql = "select st_length(geos) as my_length from test_length"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_length_curve(spark):
    data = "length_curve.csv"
    table_name = 'test_length_curve'
    sql = "select st_length(geos) as my_length from test_length_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_area(spark):
    data = "area.csv"
    table_name = 'test_area'
    sql = "select st_area(geos) as my_area from test_area"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_area_curve(spark):
    data = "area_curve.csv"
    table_name = 'test_area_curve'
    sql = "select st_area(geos) as my_area from test_area_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_distance(spark):
    data = "distance.csv"
    table_name = 'test_distance'
    sql = "select st_distance(left, right) as my_distance from test_distance"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_distance_curve(spark):
    data = "distance_curve.csv"
    table_name = 'test_distance_curve'
    sql = "select st_distance(left, right) as my_distance from test_distance_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_issimple(spark):
    data = "issimple.csv"
    table_name = 'test_issimple'
    sql = "select st_issimple(geos) from test_issimple"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_issimple_curve(spark):
    data = "issimple_curve.csv"
    table_name = 'test_issimple_curve'
    sql = "select st_issimple(geos) from test_issimple_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_npoints(spark):
    data = "npoints.csv"
    table_name = 'test_npoints'
    sql = "select st_npoints(geos) as my_npoints from test_npoints"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_geometrytype(spark):
    data = "geometrytype.csv"
    table_name = 'test_gt'
    sql = "select st_geometrytype(geos) as geos from test_gt"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()

    save_result("results/%s" % table_name, rs)

def run_test_st_geometrytype_curve(spark):
    data = "geometrytype_curve.csv"
    table_name = 'test_gt_curve'
    sql = "select st_geometrytype(geos) as geos from test_gt_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()

    save_result("results/%s" % table_name, rs)

def run_test_st_transform(spark):
    data = "transform.csv"
    table_name = 'test_transform'
    sql = "select st_transform(geos, 'epsg:4326', 'epsg:3857') as geos from test_transform"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    
    save_result("results/%s" % table_name, rs)

def run_test_st_transform1(spark):
    data = "transform.csv"
    table_name = 'test_transform1'
    sql = "select st_transform(geos, 'epsg:3857', 'epsg:4326') as geos from test_transform1"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()

    save_result("results/%s" % table_name, rs)

def run_test_st_precisionreduce(spark):
    data = "precisionreduce.csv"
    table_name = 'test_precisionreduce'
    sql = "select st_precisionreduce(geos,4) as geos from test_precisionreduce"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()

    save_result("results/%s" % table_name, rs)
    

def run_test_st_intersects(spark):
    
    data = "intersects.csv"
    table_name = 'test_intersects'
    sql = "select st_intersects(left, right) as geos from test_intersects"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_intersects_curve(spark):
    
    data = "intersects_curve.csv"
    table_name = 'test_intersects_curve'
    sql = "select st_intersects(left, right) as geos from test_intersects_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_contains(spark):
    
    data = "contains.csv"
    table_name = 'test_contains'
    sql = "select st_contains(left, right) as geos from test_contains"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_contains_curve(spark):
    
    data = "contains_curve.csv"
    table_name = 'test_contains_curve'
    sql = "select st_contains(left, right) as geos from test_contains_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_within(spark):
    
    data = "within.csv"
    table_name = 'test_within'
    sql = "select st_within(left, right) as geos from test_within"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_within_curve(spark):
    
    data = "within_curve.csv"
    table_name = 'test_within_curve'
    sql = "select st_within(left, right) as geos from test_within_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_equals_1(spark):
    
    data = "equals.csv"
    table_name = 'test_equals'
    sql = "select st_equals(left, right) as geos from test_equals"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_equals_2(spark):
    
    data = "equals2.csv"
    table_name = 'test_equals_2'
    sql = "select st_equals(st_envelope(left), right) as geos from test_equals_2"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_crosses(spark):
    
    data = "crosses.csv"
    table_name = 'test_crosses'
    sql = "select st_crosses(left, right) as geos from test_crosses"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_crosses_curve(spark):
    data = "crosses_curve.csv"
    table_name = 'test_crosses_curve'
    sql = "select st_crosses(left, right) as geos from test_crosses_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_overlaps(spark):
    
    data = "overlaps.csv"
    table_name = 'test_overlaps'
    sql = "select st_overlaps(left, right) as geos from test_overlaps"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_overlaps_curve(spark):
    
    data = "overlaps_curve.csv"
    table_name = 'test_overlaps_curve'
    sql = "select st_overlaps(left, right) as geos from test_overlaps_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_touches(spark):
    
    data = "touches.csv"
    table_name = 'test_touches'
    sql = "select st_touches(left, right) as geos from test_touches"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_touches_curve(spark):
    
    data = "touches_curve.csv"
    table_name = 'test_touches_curve'
    sql = "select st_touches(left, right) as geos from test_touches_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_makevalid(spark):
    data = "makevalid.csv"
    table_name = 'test_makevalid'
    sql = "select st_makevalid(geos) as geos from test_makevalid"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_polygonfromenvelope(spark):
    data = "polygonfromenvelope.json"
    table_name = 'test_polygonfromenvelope'
    sql = "select st_polygonfromenvelope(a, c, b, d) as geos from test_polygonfromenvelope"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_simplifypreservetopology(spark):
    data = "simplifypreservetopology.csv"
    table_name = 'test_simplifypreservetopology'
    sql = "select st_simplifypreservetopology(geos, 1) as geos from test_simplifypreservetopology"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_simplifypreservetopology_curve(spark):
    data = "simplifypreservetopology_curve.csv"
    table_name = 'test_simplifypreservetopology_curve'
    sql = "select st_curvetoline(st_simplifypreservetopology(geos, 1)) as geos from test_simplifypreservetopology_curve"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_curvetoline(spark):
    data = "curvetoline.csv"
    table_name = 'test_curvetoline'
    sql = "select st_curvetoline(geos) as geos from test_curvetoline"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_geomfromgeojson(spark):

    data = "geojson.csv"
    table_name = 'test_geomfromjson'
    sql = "select st_geomfromgeojson(geos) as geos from test_geomfromjson"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_geomfromgeojson2(spark):
    # this test is only test that arctern can handle empty geojsons, which postgis cannot, do not need to compare with postgis
    data = "geojson2.csv"
    table_name = 'test_geomfromjson2'
    sql = "select st_geomfromgeojson(geos) as geos from test_geomfromjson2"
    
    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)
    
    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_hausdorffdistance(spark):
    data = "hausdorffdistance.csv"
    table_name = 'test_hausdorffdistance'
    sql = "select st_hausdorffdistance(left,right) as geos from test_hausdorffdistance"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_hausdorffdistance_curve(spark):
    data = "hausdorffdistance_curve.csv"
    table_name = 'test_hausdorffdistance_curve'
    sql = "select st_hausdorffdistance(left,right) as geos from test_hausdorffdistance_curve"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_pointfromtext(spark):
    data = "pointfromtext.csv"
    table_name = 'test_pointfromtext'
    sql = "select st_pointfromtext(geos) as geos from test_pointfromtext"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_polygonfromtext(spark):
    data = "polygonfromtext.csv"
    table_name = 'test_polygonfromtext'
    sql = "select st_polygonfromtext(geos) as geos from test_polygonfromtext"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_linestringfromtext(spark):
    data = "linestringfromtext.csv"
    table_name = 'test_linestringfromtext'
    sql = "select st_linestringfromtext(geos) as geos from test_linestringfromtext"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_geomfromtext(spark):
    data = "geomfromtext.csv"
    table_name = 'test_geomfromtext'
    sql = "select st_geomfromtext(geos) as geos from test_geomfromtext"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_geomfromwkt(spark):
    data = "geomfromtext.csv"
    table_name = 'test_geomfromwkt'
    sql = "select st_geomfromwkt(geos) as geos from test_geomfromwkt"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

def run_test_st_astext(spark):
    data = "geomfromtext.csv"
    table_name = 'test_astext'
    sql = "select st_astext(geos) as geos from test_astext"

    df = read_data(spark, base_dir, data)
    df.printSchema()
    df.show()
    df.createOrReplaceTempView(table_name)

    rs = spark.sql(sql).cache()
    rs.printSchema()
    rs.show()
    save_result("results/%s" % table_name, rs)

if __name__ == "__main__":

    url = 'local'
    spark_session = SparkSession.builder.appName("Python zgis sample").master(url).getOrCreate()
    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    clear_result_dir('/tmp/results')
    register_funcs(spark_session)
    
    run_test_st_geomfromgeojson(spark_session)
    run_test_st_geomfromgeojson2(spark_session)
    run_test_st_curvetoline(spark_session)
    run_test_st_point(spark_session)
    run_test_envelope_aggr_1(spark_session)
    run_test_envelope_aggr_curve(spark_session)
    run_test_envelope_aggr_2(spark_session)
    run_test_union_aggr_2(spark_session)
    run_test_union_aggr_curve(spark_session)
    run_test_st_isvalid_1(spark_session)
    run_test_st_isvalid_curve(spark_session)
    run_test_st_intersection(spark_session)
    run_test_st_intersection_curve(spark_session)
    run_test_st_convexhull(spark_session)
    run_test_st_convexhull_curve(spark_session)
    run_test_st_buffer(spark_session)
    run_test_st_buffer1(spark_session)
    run_test_st_buffer2(spark_session)
    run_test_st_buffer3(spark_session)
    run_test_st_buffer4(spark_session)
    run_test_st_buffer5(spark_session)
    run_test_st_buffer6(spark_session)
    run_test_st_buffer_curve(spark_session)
    run_test_st_buffer_curve1(spark_session)
    run_test_st_envelope(spark_session)
    run_test_st_envelope_curve(spark_session)
    run_test_st_centroid(spark_session)
    run_test_st_centroid_curve(spark_session)
    run_test_st_length(spark_session)
    run_test_st_length_curve(spark_session)
    run_test_st_area(spark_session)
    run_test_st_area_curve(spark_session)
    run_test_st_distance(spark_session)
    run_test_st_distance_curve(spark_session)
    run_test_st_issimple(spark_session)
    run_test_st_issimple_curve(spark_session)
    run_test_st_npoints(spark_session)
    run_test_st_geometrytype(spark_session)
    run_test_st_geometrytype_curve(spark_session)
    run_test_st_transform(spark_session)
    run_test_st_transform1(spark_session)
    run_test_st_intersects(spark_session)
    run_test_st_intersects_curve(spark_session)
    run_test_st_contains(spark_session)
    run_test_st_contains_curve(spark_session)
    run_test_st_within(spark_session)
    run_test_st_within_curve(spark_session)
    run_test_st_equals_1(spark_session)
    run_test_st_equals_2(spark_session)
    run_test_st_crosses(spark_session)
    run_test_st_crosses_curve(spark_session)
    run_test_st_overlaps(spark_session)
    run_test_st_overlaps_curve(spark_session)
    run_test_st_touches(spark_session)
    run_test_st_touches_curve(spark_session)
    run_test_st_makevalid(spark_session)
    run_test_st_precisionreduce(spark_session)
    run_test_st_polygonfromenvelope(spark_session)
    run_test_st_simplifypreservetopology(spark_session)
    run_test_st_simplifypreservetopology_curve(spark_session)
    run_test_st_hausdorffdistance(spark_session)
    run_test_st_hausdorffdistance_curve(spark_session)
    run_test_st_pointfromtext(spark_session)
    run_test_st_polygonfromtext(spark_session)
    run_test_st_linestringfromtext(spark_session)
    run_test_st_geomfromtext(spark_session)
    run_test_st_geomfromwkt(spark_session)
    run_test_st_astext(spark_session)

    spark_session.stop()
