import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data",one_hot=True)

batch_size = 64
n_batch = mnist.train.num_examples // batch_size

x = tf.placeholder(tf.float32,[None,784])
y = tf.placeholder(tf.float32,[None,10])
keep_prob = tf.placeholder(tf.float32)
Ir = tf.Variable(0.001,tf.float32)

W1 = tf.Variable(tf.truncated_normal([784,500],stddev=0.1))
b1 = tf.Variable(tf.zeros([1,500])+0.1)
L1 = tf.nn.relu(tf.matmul(x,W1)+b1)
L1_prob = tf.nn.dropout(L1,keep_prob)

W2 = tf.Variable(tf.truncated_normal([500,300],stddev=0.1))
b2 = tf.Variable(tf.zeros([1,300])+0.1)
L2 = tf.nn.relu(tf.matmul(L1_prob,W2)+b2)
L2_prob = tf.nn.dropout(L2,keep_prob)

W3 = tf.Variable(tf.truncated_normal([300,10],stddev=0.1))
b3 = tf.Variable(tf.zeros([1,10])+0.1)
prediction = tf.nn.softmax(tf.matmul(L2_prob,W3)+b3)

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction))
train_step = tf.train.AdamOptimizer(Ir).minimize(loss)

init = tf.global_variables_initializer()

correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(prediction,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

#创建一个会话
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(31):
        sess.run(tf.assign(Ir,0.001*(0.95**(epoch))))
        for batch in range(n_batch): 
            batch_xs,batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys,keep_prob:0.7})
            
        learning_rate = sess.run(Ir)
        acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,keep_prob:1.0})
        
        print("Iter " + str(epoch) + ", Testing Accuracy = " + str(acc) + ", Learning Rate=" + str(learning_rate))