import express from "express";
import connectDB from "./connect.js";
import dotenv from "dotenv";
import userRoutes from "./routes/auth.js"; // adjust path if needed
import cors from "cors";
import multer from "multer"; // 📦 for file uploads
import path from "path";
import fs from "fs";
import UserProfile from "./models/userProfile.js"; // ✅ import model

dotenv.config();

const app = express();

app.use(cors({
  origin: "http://127.0.0.1:5500",
  methods: ["GET", "POST", "PUT", "DELETE"],
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

connectDB();

// 📂 Serve static uploaded images
app.use("/uploads", express.static(path.join(path.resolve(), "uploads")));

// 🔧 Multer setup
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadDir = "uploads";
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir);
    }
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + "-" + file.originalname);
  }
});
const upload = multer({ storage: storage });

// ROUTES
app.use("/api", userRoutes);

// ✅ Profile upload and save route
app.post("/api/profile", upload.single("profilePic"), async (req, res) => {
  const { username, email, phone } = req.body;
  const profilePicPath = req.file ? `/uploads/${req.file.filename}` : null;

  try {
    // ✅ Save to MongoDB
    const newProfile = new UserProfile({
      username,
      email,
      phone,
      profilePicPath
    });

    await newProfile.save();

    console.log("📦 Saved to MongoDB:", newProfile);

    res.json({
      success: true,
      message: "Profile saved successfully",
      data: newProfile
    });

  } catch (err) {
    console.error("❌ Error saving profile:", err);
    res.status(500).json({
      success: false,
      message: "Failed to save profile"
    });
  }
});

app.listen(5000, () => {
  console.log("🚀 Server running at http://localhost:5000");
});  