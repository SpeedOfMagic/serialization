package serialization;

import java.io.*;

import objects.Evaluatable;

public class LanguageSerializer implements Serializer {
    @Override
    public void SerializeToFile(Evaluatable o, String filePath) {
        try {
            Serializable obj = (Serializable) o;
            ObjectOutputStream objectOutputStream = new ObjectOutputStream(
                new FileOutputStream(filePath)
            );
            objectOutputStream.writeObject(obj);
            objectOutputStream.close();
        } catch (FileNotFoundException e) {
            System.err.println("Could not find file " + filePath);
            e.printStackTrace();
        } catch (IOException e) {
            System.err.println("IOException while serializing to file " + filePath);
            e.printStackTrace();
        }
    }

    @Override
    public Evaluatable DeserializeFromFile(String filePath) {
        try {
            ObjectInputStream objectInputStream = new ObjectInputStream(
                new FileInputStream(filePath)
            );
            Evaluatable objRestored = (Evaluatable) objectInputStream.readObject();
            objectInputStream.close();
            return objRestored;
        } catch (FileNotFoundException e) {
            System.err.println("Could not find file " + filePath);
            e.printStackTrace();
        } catch (IOException e) {
            System.err.println("IOException while deserializing to file " + filePath);
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            System.err.println("Could not find class while deserializing file " + filePath);
            e.printStackTrace();
        }
        return null;
    }
}
