import mongoose from "mongoose";

const userProfileSchema = new mongoose.Schema({
  username: String,
  email: String,
  phone: String,
  profilePicPath: String  // 👈 stores "/uploads/filename.jpg"
});

const UserProfile = mongoose.model("UserProfile", userProfileSchema);
export default UserProfile;
        