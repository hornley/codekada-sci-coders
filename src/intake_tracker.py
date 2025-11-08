"""
Intake Tracker - Phase 3
Tracks consumed products over time using SQLite database.
"""

import sqlite3
import json
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from src.models import ProductAnalysisResponse, UserHealthPreferences


class IntakeTracker:
    """Tracks product consumption history and provides health insights."""
    
    def __init__(self, db_path: str = "intake_history.db"):
        """
        Initialize the intake tracker.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create intake_log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intake_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                product_name TEXT,
                product_type TEXT NOT NULL,
                ingredients_text TEXT,
                harmful_ingredients TEXT,
                allergens TEXT,
                additives TEXT,
                preservatives TEXT,
                healthiness_rating INTEGER,
                safety_score_for_user INTEGER,
                matches_preferences INTEGER,
                recommendation TEXT,
                personalized_recommendation TEXT,
                full_analysis TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Create user_preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                allergies TEXT,
                dietary_restrictions TEXT,
                avoid_ingredients TEXT,
                health_goals TEXT,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Create health_metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                total_products INTEGER DEFAULT 0,
                avg_health_rating REAL,
                harmful_count INTEGER DEFAULT 0,
                allergen_exposures INTEGER DEFAULT 0,
                preference_violations INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_intake(
        self,
        analysis_result: ProductAnalysisResponse,
        timestamp: Optional[datetime] = None
    ) -> int:
        """
        Log a consumed product to the database.
        
        Args:
            analysis_result: Product analysis response
            timestamp: When product was consumed (defaults to now)
            
        Returns:
            ID of the logged entry
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert lists to JSON strings
        harmful_ingredients = json.dumps(analysis_result.harmful_ingredients)
        allergens = json.dumps(analysis_result.allergens)
        additives = json.dumps(analysis_result.additives)
        preservatives = json.dumps(analysis_result.preservatives)
        full_analysis = analysis_result.model_dump_json()
        
        cursor.execute("""
            INSERT INTO intake_log (
                timestamp, product_name, product_type, ingredients_text,
                harmful_ingredients, allergens, additives, preservatives,
                healthiness_rating, safety_score_for_user, matches_preferences,
                recommendation, personalized_recommendation, full_analysis, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp.isoformat(),
            analysis_result.product_name,
            analysis_result.product_type,
            analysis_result.ingredients_text,
            harmful_ingredients,
            allergens,
            additives,
            preservatives,
            analysis_result.healthiness_rating,
            analysis_result.safety_score_for_user,
            1 if analysis_result.matches_preferences else 0 if analysis_result.matches_preferences is not None else None,
            analysis_result.recommendation,
            analysis_result.personalized_recommendation,
            full_analysis,
            datetime.now().isoformat()
        ))
        
        entry_id = cursor.lastrowid
        
        # Update daily metrics
        self._update_daily_metrics(cursor, timestamp.date(), analysis_result)
        
        conn.commit()
        conn.close()
        
        return entry_id
    
    def _update_daily_metrics(
        self,
        cursor: sqlite3.Cursor,
        date: Any,
        analysis: ProductAnalysisResponse
    ):
        """Update daily health metrics."""
        date_str = date.isoformat()
        
        # Get existing metrics
        cursor.execute(
            "SELECT total_products, avg_health_rating, harmful_count, allergen_exposures, preference_violations FROM health_metrics WHERE date = ?",
            (date_str,)
        )
        row = cursor.fetchone()
        
        if row:
            total_products, avg_rating, harmful_count, allergen_exposures, preference_violations = row
            new_total = total_products + 1
            new_avg = ((avg_rating * total_products) + analysis.healthiness_rating) / new_total
            new_harmful = harmful_count + (1 if analysis.harmful_ingredients else 0)
            new_allergens = allergen_exposures + (1 if analysis.allergens else 0)
            new_violations = preference_violations + (1 if analysis.matches_preferences is False else 0)
            
            cursor.execute("""
                UPDATE health_metrics
                SET total_products = ?, avg_health_rating = ?, harmful_count = ?,
                    allergen_exposures = ?, preference_violations = ?
                WHERE date = ?
            """, (new_total, new_avg, new_harmful, new_allergens, new_violations, date_str))
        else:
            cursor.execute("""
                INSERT INTO health_metrics (
                    date, total_products, avg_health_rating, harmful_count,
                    allergen_exposures, preference_violations
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                date_str,
                1,
                float(analysis.healthiness_rating),
                1 if analysis.harmful_ingredients else 0,
                1 if analysis.allergens else 0,
                1 if analysis.matches_preferences is False else 0
            ))
    
    def get_daily_summary(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get summary of intake for a specific day.
        
        Args:
            date: Date to summarize (defaults to today)
            
        Returns:
            Summary dictionary
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.date().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all entries for the day
        cursor.execute("""
            SELECT product_name, product_type, healthiness_rating,
                   harmful_ingredients, allergens, matches_preferences
            FROM intake_log
            WHERE DATE(timestamp) = ?
            ORDER BY timestamp
        """, (date_str,))
        
        entries = cursor.fetchall()
        
        # Get metrics
        cursor.execute(
            "SELECT * FROM health_metrics WHERE date = ?",
            (date_str,)
        )
        metrics_row = cursor.fetchone()
        
        conn.close()
        
        # Build summary
        products = []
        for entry in entries:
            products.append({
                'product_name': entry[0],
                'product_type': entry[1],
                'healthiness_rating': entry[2],
                'harmful_ingredients': json.loads(entry[3]) if entry[3] else [],
                'allergens': json.loads(entry[4]) if entry[4] else [],
                'matches_preferences': bool(entry[5]) if entry[5] is not None else None
            })
        
        summary = {
            'date': date_str,
            'total_products': len(products),
            'products': products,
            'metrics': None
        }
        
        if metrics_row:
            summary['metrics'] = {
                'total_products': metrics_row[2],
                'avg_health_rating': round(metrics_row[3], 2) if metrics_row[3] else 0,
                'harmful_count': metrics_row[4],
                'allergen_exposures': metrics_row[5],
                'preference_violations': metrics_row[6]
            }
        
        return summary
    
    def get_weekly_report(self, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get 7-day health report.
        
        Args:
            end_date: End date for report (defaults to today)
            
        Returns:
            Weekly report dictionary
        """
        if end_date is None:
            end_date = datetime.now()
        
        start_date = end_date - timedelta(days=6)  # 7 days including end_date
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get daily metrics for the week
        cursor.execute("""
            SELECT date, total_products, avg_health_rating, harmful_count,
                   allergen_exposures, preference_violations
            FROM health_metrics
            WHERE date >= ? AND date <= ?
            ORDER BY date
        """, (start_date.date().isoformat(), end_date.date().isoformat()))
        
        daily_metrics = cursor.fetchall()
        
        # Get all products in the week
        cursor.execute("""
            SELECT product_name, product_type, healthiness_rating, harmful_ingredients
            FROM intake_log
            WHERE DATE(timestamp) >= ? AND DATE(timestamp) <= ?
            ORDER BY timestamp
        """, (start_date.date().isoformat(), end_date.date().isoformat()))
        
        all_products = cursor.fetchall()
        
        conn.close()
        
        # Calculate weekly stats
        total_products = len(all_products)
        avg_health_rating = sum(p[2] for p in all_products) / total_products if total_products > 0 else 0
        total_harmful = sum(1 for p in all_products if (json.loads(p[3]) if p[3] else []))
        
        # Build daily breakdown
        daily_breakdown = []
        for row in daily_metrics:
            daily_breakdown.append({
                'date': row[0],
                'total_products': row[1],
                'avg_health_rating': round(row[2], 2) if row[2] else 0,
                'harmful_count': row[3],
                'allergen_exposures': row[4],
                'preference_violations': row[5]
            })
        
        return {
            'period': f"{start_date.date().isoformat()} to {end_date.date().isoformat()}",
            'total_products': total_products,
            'avg_health_rating': round(avg_health_rating, 2),
            'total_harmful_exposures': total_harmful,
            'daily_breakdown': daily_breakdown
        }
    
    def get_all_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get intake history.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of intake entries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, product_name, product_type, healthiness_rating,
                   harmful_ingredients, allergens, recommendation
            FROM intake_log
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        entries = cursor.fetchall()
        conn.close()
        
        history = []
        for entry in entries:
            history.append({
                'timestamp': entry[0],
                'product_name': entry[1],
                'product_type': entry[2],
                'healthiness_rating': entry[3],
                'harmful_ingredients': json.loads(entry[4]) if entry[4] else [],
                'allergens': json.loads(entry[5]) if entry[5] else [],
                'recommendation': entry[6]
            })
        
        return history
    
    def check_product_against_history(
        self,
        product_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Check if a product has been consumed before.
        
        Args:
            product_name: Name of product to check
            
        Returns:
            Previous consumption data if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, healthiness_rating, recommendation, full_analysis
            FROM intake_log
            WHERE LOWER(product_name) = LOWER(?)
            ORDER BY timestamp DESC
            LIMIT 1
        """, (product_name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'last_consumed': row[0],
                'healthiness_rating': row[1],
                'recommendation': row[2],
                'full_analysis': json.loads(row[3]) if row[3] else None
            }
        
        return None
    
    def save_user_preferences(self, preferences: UserHealthPreferences):
        """
        Save user health preferences to database.
        
        Args:
            preferences: User health preferences
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old preferences
        cursor.execute("DELETE FROM user_preferences")
        
        # Insert new preferences
        cursor.execute("""
            INSERT INTO user_preferences (
                allergies, dietary_restrictions, avoid_ingredients,
                health_goals, updated_at
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            json.dumps(preferences.allergies),
            json.dumps(preferences.dietary_restrictions),
            json.dumps(preferences.avoid_ingredients),
            json.dumps(preferences.health_goals),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def load_user_preferences(self) -> Optional[UserHealthPreferences]:
        """
        Load user health preferences from database.
        
        Returns:
            UserHealthPreferences if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT allergies, dietary_restrictions, avoid_ingredients, health_goals
            FROM user_preferences
            ORDER BY id DESC
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return UserHealthPreferences(
                allergies=json.loads(row[0]) if row[0] else [],
                dietary_restrictions=json.loads(row[1]) if row[1] else [],
                avoid_ingredients=json.loads(row[2]) if row[2] else [],
                health_goals=json.loads(row[3]) if row[3] else []
            )
        
        return None
    
    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete an intake entry.
        
        Args:
            entry_id: ID of entry to delete
            
        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM intake_log WHERE id = ?", (entry_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def clear_history(self, confirm: bool = False):
        """
        Clear all intake history.
        
        Args:
            confirm: Must be True to actually clear
        """
        if not confirm:
            raise ValueError("Must confirm=True to clear all history")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM intake_log")
        cursor.execute("DELETE FROM health_metrics")
        
        conn.commit()
        conn.close()


if __name__ == "__main__":
    # Test the intake tracker
    print("Testing IntakeTracker...")
    
    tracker = IntakeTracker("test_intake.db")
    print("✓ Database initialized")
    
    # Test user preferences
    from src.models import UserHealthPreferences
    prefs = UserHealthPreferences(
        allergies=["peanuts"],
        dietary_restrictions=["vegan"],
        health_goals=["weight loss"]
    )
    tracker.save_user_preferences(prefs)
    print("✓ User preferences saved")
    
    loaded_prefs = tracker.load_user_preferences()
    print(f"✓ User preferences loaded: {loaded_prefs.allergies}")
    
    print("\n✅ IntakeTracker test complete!")
