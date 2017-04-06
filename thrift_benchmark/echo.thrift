/**
 * The first thing to know about are types. The available types in Thrift are:
 *
 *  bool        Boolean, one byte
 *  i8 (byte)   Signed 8-bit integer
 *  i16         Signed 16-bit integer
 *  i32         Signed 32-bit integer
 *  i64         Signed 64-bit integer
 *  double      64-bit floating point value
 *  string      String
 *  binary      Blob (byte array)
 *  map<t1,t2>  Map from one type to another
 *  list<t1>    Ordered list of one type
 *  set<t1>     Set of unique elements of one type
 *
 * Did you also notice that Thrift supports C style comments?
 */

namespace py echo

struct Packet {
    1: required string ride_id;
    2: required string workout_id;
    3: required i16 seconds_since_pedaling_start;
    4: required double total_work;
}

service Echo {

   string echo(string s),
   void add(Packet p),
   map<i16, i16> count(),
   bool reset()

}
