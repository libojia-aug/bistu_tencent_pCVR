import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.Optional;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.PairFunction;
import scala.Tuple2;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by Berger on 2017/6/5.
 */

public class usersFC {

    public static void main(String[] args) throws Exception {
        SparkConf sparkConf = new SparkConf().setAppName("tablesjoin").setMaster("local");
        JavaSparkContext sc = new JavaSparkContext(sparkConf);
        JavaRDD<String> text1 = sc.textFile("./input/user_installedapps.csv");
        JavaPairRDD<String, String> pairRDD1 = text1.mapToPair(
                new PairFunction<String, String, String>() {
                    private static final long serialVersionUID = 1L;

                    public Tuple2<String, String> call(String line) throws Exception {
                        String[] arr = line.split(",");
                        return new Tuple2<String, String>(arr[0], arr[1]);
                    }
                });
        pairRDD1.combineByKey(
                new Function<Tuple2<String,String>, Integer>() {
                    public Integer call(Tuple2<String,String> line) throws Exception {
                        line._2()
                        return new Tuple2<String, String>(arr[0], arr[1]);
                    }
                }
        )
//        pairRDD3.leftOuterJoin(pairRDDTmp).sortByKey().saveAsTextFile("./output/cuser-c-g");
//        pairRDD4.leftOuterJoin(pairRDDTmp).sortByKey().saveAsTextFile("./output/ncuser-c-g");
        sc.close();
    }
}
