/**
 * Created by Berger on 2017/6/4.
 */

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.Optional;
import org.apache.spark.api.java.function.PairFunction;
import scala.Tuple2;

public class tableJoin {
    public tableJoin() {
    }

    public static void main(String[] args) throws Exception {
        SparkConf sparkConf = new SparkConf().setAppName("tablesjoin").setMaster("local");
        JavaSparkContext sc = new JavaSparkContext(sparkConf);
        JavaRDD<String> text1 = sc.textFile("./input/app_categories.csv");
        JavaRDD<String> text2 = sc.textFile("./input/user_installedapps.csv");
        JavaRDD<String> text3 = sc.textFile("./input/CUsers.csv");
        JavaRDD<String> text4 = sc.textFile("./input/NCUsers.csv");
        JavaPairRDD<String, String> pairRDD1 = text1.mapToPair(
                new PairFunction<String, String, String>() {
                    private static final long serialVersionUID = 1L;

                    public Tuple2<String, String> call(String line) throws Exception {
                        String[] arr = line.split(",");
                        return new Tuple2<String, String>(arr[0], arr[1]);
                    }
                });
        JavaPairRDD<String, String> pairRDD2 = text2.mapToPair(
                new PairFunction<String, String, String>() {
                    private static final long serialVersionUID = 1L;

                    public Tuple2<String, String> call(String line) throws Exception {
                        String[] arr = line.split(",");
                        return new Tuple2<String, String>(arr[1], arr[0]);
                    }
                });
        JavaPairRDD<String, String> pairRDD3 = text3.mapToPair(
                new PairFunction<String, String, String>() {
                    private static final long serialVersionUID = 1L;

                    public Tuple2<String, String> call(String line) throws Exception {
                        String[] arr = line.split(",");
                        return new Tuple2<String, String>(arr[4], "");
                    }
                });
        JavaPairRDD<String, String> pairRDD4 = text4.mapToPair(
                new PairFunction<String, String, String>() {
                    private static final long serialVersionUID = 1L;

                    public Tuple2<String, String> call(String line) throws Exception {
                        String[] arr = line.split(",");
                        return new Tuple2<String, String>(arr[4], "");
                    }
                });
//        pairRDD1.rightOuterJoin(pairRDD2).saveAsTextFile("./output/user-cate-a");
//        pairRDD1.rightOuterJoin(pairRDD2).values().saveAsTextFile("./output/user-cate-v");
//        pairRDD2.leftOuterJoin(pairRDD1).values().saveAsTextFile("./output/user-cate-v");
        JavaPairRDD<String, Iterable<String>> pairRDDTmp = pairRDD2.leftOuterJoin(pairRDD1).values().mapToPair(
                new PairFunction<Tuple2<String, Optional<String>>, String, String>() {
                    private static final long serialVersionUID = 1L;

                    public Tuple2<String, String> call(Tuple2<String, Optional<String>> line) throws Exception {

                        return new Tuple2<String, String>(line._1, line._2.toString());
                    }
                }).groupByKey();
        pairRDD3.leftOuterJoin(pairRDDTmp).count();
        pairRDD4.leftOuterJoin(pairRDDTmp).count();
//        pairRDD3.leftOuterJoin(pairRDDTmp).sortByKey().saveAsTextFile("./output/cuser-c-g");
//        pairRDD4.leftOuterJoin(pairRDDTmp).sortByKey().saveAsTextFile("./output/ncuser-c-g");
        sc.close();
    }
}
